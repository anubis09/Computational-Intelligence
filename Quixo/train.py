import numpy as np
from game import Game, Move
from players import RLayer
from collections import defaultdict


class ValueIteration(RLayer):
    def __init__(self) -> None:
        super().__init__()
        self.lr = 0.1
        self.gamma_decay = 0.9
        self.policy = defaultdict(float)

    # In questo momento abbiamo una funziona che restituisce tutte le mosse possibili.
    # Se non andasse bene, dovremmo aggiungerla nella subclass del game.
    # E poi il nostro state value dovrebbe diventare un dict di dict.
    # High level dict con lo stato di partenza, poi ci associamo un dict con tutte le mosse che ha esplorato il modello.
    # If no moves available?? Potremmo farlo giocare a caso.
    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        return super().make_move(game)

    def back_prop(self, reward: int):
        """
        The back_prop function is responsible for updating the policy values in the agent's memory during the training process.
        It adjusts the policy values based on the received reward.
        """
        for state in reversed(self._game_state):
            # state is an hash of next_board
            self.policy[state] += self.lr * (
                self.gamma_decay * reward - self.policy[state]
            )
            reward = self.policy[state]
        self._game_state = []

    def save_policy(self, name):
        return super().save_policy(name)


if __name__ == "__main__":
    v = ValueIteration()
    v.save_policy("ciao")
