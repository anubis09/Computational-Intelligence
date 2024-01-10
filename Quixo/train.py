import numpy as np
from game import Game, Move
from players import RLayer
from collections import defaultdict
import os
import json


class KeyValuePolicy(RLayer):
    def __init__(self) -> None:
        super().__init__()
        self._epsilon = 0.3
        self._game_moves = []
        self._lr = 0.1
        self._gamma_decay = 0.9
        self._policy = defaultdict(float)

    # In questo momento abbiamo una funziona che restituisce tutte le mosse possibili.
    # Se non andasse bene, dovremmo aggiungerla nella subclass del game.
    # E poi il nostro state value dovrebbe diventare un dict di dict.
    # High level dict con lo stato di partenza, poi ci associamo un dict con tutte le mosse che ha esplorato il modello.
    # If no moves available?? Potremmo farlo giocare a caso.
    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        possible_moves = game.possible_moves()
        if np.random.random() < self._epsilon:
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
                if self._policy[key] > best_value:
                    best_move = move
                    best_value = self._policy[key]
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
        json.dump(self._policy, f)

    def value_iteration_back_prop(self, reward: int):
        """
        The back_prop function is responsible for updating the policy values in the agent's memory during the training process.
        It adjusts the policy values based on the received reward.
        """
        for state in reversed(self._game_state):
            # state is an hash of next_board
            self._policy[state] += self._lr * (
                self._gamma_decay * reward - self._policy[state]
            )
            reward = self._policy[state]
        self._game_state = []


if __name__ == "__main__":
    v = KeyValuePolicy()
    v.save_policy("ciao")
