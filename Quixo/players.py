import random
from game import Game, Move, Player
import numpy as np
import os
import json


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: "Game") -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class RLayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.train_mode = False
        self._epsilon = 0.3
        self._game_moves = []
        self.policy = {}  # TODO import the state value policy

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        possible_moves = game.possible_moves()
        if self.train_mode and np.random.random() < self._epsilon:
            # exploration phase
            index = np.random.choice(len(possible_moves))
            move = possible_moves[index]
            self._game_moves.append(
                (str(game.get_board), move)
            )  # board hashing
            return move
        else:
            # selects the best move in the policy.
            best_move = None
            board_hash = str(game.get_board)
            best_value = float("-inf")
            for move in possible_moves:
                key = (board_hash, move)
                if self.policy[key] > best_value:
                    best_move = move
                    best_value = self.policy[key]
            if self.train_mode:
                self._game_moves.append((board_hash, best_move))
            return best_move

    def save_policy(self, name):
        """
        It saves the policy
        """
        path = os.path.join("Quixo", "Policies")
        if not os.path.exists(path):
            os.makedirs(path)
        filename = "policy_" + name + ".json"
        f = open(os.path.join(path, filename), "w")
        json.dump(self.policy, f)


class HumanPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: "Game") -> tuple[tuple[int, int], Move]:
        print(
            "Remember the convention: X goes left to right, Y goes top to bottom."
        )
        # print(game.get_possible_moves())
        inp = input(
            "insert the X and Y coordinate in the format: 'x y': "
        ).strip()
        x, y = (int(coord) for coord in inp.split(" "))
        move = input("insert the slide move (TOP,LEFT,BOTTOM,RIGHT): ")
        match move.upper():
            case "TOP":
                slide = Move.TOP
            case "LEFT":
                slide = Move.LEFT
            case "BOTTOM":
                slide = Move.BOTTOM
            case _:
                slide = Move.RIGHT
        # da capire
        return (x, y), slide
