import numpy as np
from game import Game, Move, Player
from players import RLayer, RandomPlayer
import os
import json
from tqdm import tqdm


class KeyValuePolicyTrainer(RLayer):
    def __init__(self, is_Q_learn: bool) -> None:
        super().__init__(None)
        self._epsilon = 0.3
        self._game_moves = []
        self._lr = 0.1
        self._gamma_decay = 0.9
        self.is_Q_learn = is_Q_learn

    # In questo momento abbiamo una funziona che restituisce tutte le mosse possibili.
    # Se non andasse bene, dovremmo aggiungerla nella subclass del game.
    # E poi il nostro state value dovrebbe diventare un dict di dict.
    # High level dict con lo stato di partenza, poi ci associamo un dict con tutte le mosse che ha esplorato il modello.
    # If no moves available?? Potremmo farlo giocare a caso.
    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        possible_moves = game.get_possible_moves()
        board_hash = game.get_hash()
        if np.random.random() < self._epsilon:
            # exploration phase
            index = np.random.choice(len(possible_moves))
            move = possible_moves[index]
            self._game_moves.append((board_hash, move))
            return move
        else:
            # selects the best move in the policy.
            best_move = super().make_move(game)
            self._game_moves.append((board_hash, best_move))
            return best_move

    def back_prop(self, reward: int) -> None:
        if self.is_Q_learn:
            self.q_learn_back_prop(reward)
        else:
            self.value_iteration_back_prop(reward)

    def value_iteration_back_prop(self, reward: int) -> None:
        """
        The back_prop function is responsible for updating the policy values in the agent's memory during the training process.
        It adjusts the policy values based on the received reward.
        """
        for state in reversed(self._game_moves):
            # state is an hash of next_board
            self._policy[state] += self._lr * (
                self._gamma_decay * reward - self._policy[state]
            )
            reward = self._policy[state]
        self._game_moves = []

    def q_learn_back_prop(self, reward: int) -> None:
        pass

    def save_policy(self, name) -> None:
        """
        It saves the policy
        """
        path = os.path.join("Quixo", "Policies")
        if not os.path.exists(path):
            os.makedirs(path)
        filename = "policy_" + name + ".json"
        f = open(os.path.join(path, filename), "w")
        json.dump(self._policy, f)


class Game_trainer(Game):
    def __init__(self) -> None:
        super().__init__()

    def print(self) -> None:
        # os.system("cls||clear")
        pass

    # look at the problem of the starting position.
    # The idea could be to leave the play as it is, then we can make our players play as first then as second.
    # we can also make array players shuffle. -> i'll go with this solution
    def train(self, trainee: Player, trainer: Player, epochs: int) -> None:
        players = [trainee, trainer]
        winning_reward = 1
        losing_reward = -1
        bar = tqdm(total=epochs, desc="Epoch")
        for _ in range(epochs):
            # np.random.shuffle(players)
            winner_idx = self.play(players[0], players[1])
            if winner_idx != -1:
                if isinstance(players[winner_idx], RLayer):
                    players[winner_idx].back_prop(winning_reward)
                loser_idx = (winner_idx + 1) % 2
                if isinstance(players[loser_idx], RLayer):
                    players[loser_idx].back_prop(losing_reward)
            bar.update(1)
        # trainee.save_policy("value_it")


if __name__ == "__main__":
    player = KeyValuePolicyTrainer(is_Q_learn=False)
    g = Game_trainer()
    g.train(player, RandomPlayer(), 1000)
