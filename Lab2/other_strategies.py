import logging
from collections import namedtuple
import random
from numpy.random import normal
from collections import defaultdict
from copy import deepcopy
import numpy as np
from pprint import pprint, pformat

# -----------------------------------

Nimply = namedtuple("Nimply", "row, num_objects")


class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects


def nim_sum(state: Nim) -> int:
    # tmp: for each row, transform the number of object in that row to its binary form (width 32 bit), binary as a tuple of bits
    tmp = np.array([tuple(int(x) for x in f"{c:032b}") for c in state.rows])
    xor = tmp.sum(axis=0) % 2
    return int(
        "".join(str(_) for _ in xor), base=2
    )  # convert the string of bit in its integer form


def analize(raw: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = dict()
    for ply in (
        Nimply(r, o) for r, c in enumerate(raw.rows) for o in range(1, c + 1)
    ):
        tmp = deepcopy(raw)
        tmp.nimming(ply)
        cooked["possible_moves"][ply] = nim_sum(tmp)
    return cooked


def optimal(state: Nim) -> Nimply:
    analysis = analize(state)
    logging.debug(f"analysis:\n{pformat(analysis)}")
    spicy_moves = [
        ply for ply, ns in analysis["possible_moves"].items() if ns != 0
    ]
    if not spicy_moves:
        spicy_moves = list(analysis["possible_moves"].keys())
    ply = random.choice(spicy_moves)
    return ply


# ------------------------------------


def all_possible_moves(state: Nim) -> list:
    all_moves = []
    for row in [r for r, c in enumerate(state.rows) if c > 0]:
        upper_bound_for = (
            min(state.rows[row], state._k) + 1
            if state._k
            else state.rows[row] + 1
        )
        for obj_to_take in range(1, upper_bound_for):
            all_moves.append(Nimply(row, obj_to_take))
    return all_moves


def pure_random(state: Nim) -> Nimply:
    """A completely random move"""
    return random.choice(all_possible_moves(state))


# for convienience and for code reusability we will implement this code as a class
class Ev_strat_1:
    def __init__(self, c_sigma: int = 1):
        self.c_sigma = c_sigma
        self.__name__ = "Ev_strat_1"

    def __call__(self, state: Nim) -> Nimply:
        cooked = dict()
        created_off = 0
        # generate lambda new states, porportional to number of object in row
        for idx_row, row in enumerate(state.rows):
            # do C*row tweaks on this row
            n_tweaks = 2 * row
            created_off += n_tweaks
            for _ in range(n_tweaks):
                n_obj_offspring = self.tweak(row)
                tmp = deepcopy(state)
                ply = Nimply(idx_row, n_obj_offspring)
                try:
                    tmp.nimming(
                        ply
                    )  # nimming already checks if currecnt move (ply) and current state are valid
                    if ply.num_objects > 0 and ply not in cooked.keys():
                        # this is the fitness function that evaluates the cooked[ply] move.
                        cooked[ply] = nim_sum(tmp)
                except:
                    pass

        # select best choice in cooked[ply].
        if cooked:
            best_ply, _ = max(cooked.items(), key=lambda t: t[1])
            # conto il numero di soluzioni "buone" trovate, se sono meno del 20% allora abbasso il sigma.
            # abbasso il sigma perchè alzandolo ci sono più probabilità di creare soluzioni fuori range.
            nim_diff_from_0 = 0
            for it in cooked.items():
                if it[1] != 0:
                    nim_diff_from_0 += 1
            if nim_diff_from_0 / created_off <= 0.2:
                self.c_sigma /= 1.1
            else:
                self.c_sigma *= 1.1
        else:  # if no cooked move, then random move
            best_ply = pure_random(state)

        return best_ply

    def tweak(self, item: int) -> list:
        starting_move = item / 2  # for now we will take the real num.
        # offspring = round(normal(loc=starting_move, scale=C_sigma * starting_move))
        offspring = round(
            normal(loc=starting_move, scale=self.c_sigma * starting_move)
        )
        # offsprings = round(normal(loc=starting_move, scale=C_sigma*starting_move, size=(C*item)))
        return offspring


def fitness(
    state: Nim,
    moves: list,
    n_games_per_move: int = 5,
    adversarial_strategy: callable = pure_random,
) -> dict:
    evaluated_moves = defaultdict(int)
    # we will play approximately for each move 10 games in which that move will be the starting one.
    for first_move in moves:
        for _ in range(n_games_per_move):
            nim = deepcopy(state)
            strategy = (pure_random, adversarial_strategy)
            # player is 0 because we are the one that moves.
            player = 0
            # first_move = random.choice(moves)
            is_first = True
            while nim:
                if is_first:
                    ply = first_move
                    is_first = False
                else:
                    ply = strategy[player](nim)
                nim.nimming(ply)
                player = 1 - player
            # add 1 to the first move value if we won with that move, 0 else
            evaluated_moves[first_move] += 1 if player == 0 else 0
    return evaluated_moves


def approximate_es(state: Nim) -> Nimply:
    all_moves = all_possible_moves(state)
    n_games_per_move = 10
    first_moves = fitness(state, all_moves, n_games_per_move=n_games_per_move)
    best_move, _ = max(first_moves.items(), key=lambda i: i[1])
    return best_move


# This es is a boost of es2:
# Cheoosen the K best moves against pure_random,
# it plays them against optimal and test which one is better


def approximate_es_boosted(state: Nim) -> Nimply:
    all_moves = all_possible_moves(state)
    first_moves = fitness(state, all_moves)
    # get top-K moves against pure_random
    K = 4
    first_moves = first_moves.items()
    top_K_first_moves = sorted(first_moves, key=lambda t: -t[1])[:K]
    top_K_first_moves = [move[0] for move in top_K_first_moves]

    n_games_per_move = 10
    moves_wins_against_optimal = fitness(
        state, top_K_first_moves, n_games_per_move, optimal
    )
    best_move, _ = max(moves_wins_against_optimal.items(), key=lambda i: i[1])

    return best_move
