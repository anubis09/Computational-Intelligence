import numpy as np
from game import Game, Move, Player
from players import RLayer, RandomPlayer, HumanPlayer
import os
import json
from tqdm import tqdm
import pprint


class KeyValuePolicyTrainer(RLayer):
    def __init__(self, is_Q_learn: bool) -> None:
        super().__init__(None)
        self._epsilon = 0.3
        self._game_moves = []
        self._lr = 0.1
        self._gamma_decay = 0.9
        self.is_Q_learn = is_Q_learn

    def make_move(self, game: "GameTrainer") -> tuple[tuple[int, int], Move]:
        possible_moves = game.get_possible_moves()
        board_hash = str(game.get_board())
        if np.random.random() < self._epsilon:
            # exploration phase
            index = np.random.choice(len(possible_moves))
            move = possible_moves[index]
            self._game_moves.append((board_hash, str(move)))
            return move
        else:
            # selects the best move in the policy.
            best_move = None
            best_value = float("-inf")
            for move in possible_moves:
                if self._policy[board_hash][str(move)] > best_value:
                    best_move = move
                    best_value = self._policy[board_hash][str(move)]
            self._game_moves.append((board_hash, str(best_move)))
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
            # state tuple(board, move)
            board = state[0]
            move = state[1]
            self._policy[board][move] += self._lr * (
                self._gamma_decay * reward - self._policy[board][move]
            )
            reward = self._policy[board][move]
        self._game_moves = []

    def q_learn_back_prop(self, reward: int) -> None:
        pass

    def n_explored_states(self):
        # states different from zero.
        counter = 0
        for k, v in self._policy.items():
            if v != 0:
                counter += 1
        return counter, len(self._policy.keys())

    def save_policy(self, name) -> None:
        """
        It saves the policy
        """
        path = os.path.join("Quixo", "Policies")
        if not os.path.exists(path):
            os.makedirs(path)
        filename = "policy_" + name + ".json"
        f = open(os.path.join(path, filename), "w")
        json.dump(self._policy, f, indent=4)


class GameTrainer(Game):
    def __init__(self) -> None:
        super().__init__()

    def print(self) -> None:
        # os.system("cls||clear")
        pass

    def get_possible_moves(self):
        # __acceptable_slides -> prende from_pos e ritorna le slides possibili.
        # for solo sugli element di contorno. e prendiamo le posizion. poi abbiamo acceptable_slides che ci dice le slide possivbili.
        moves = []
        for row in [0, 4]:
            for col in range(5):
                if (
                    self._board[row, col] == self.current_player_idx
                    or self._board[row, col] == -1
                ):
                    slides = self._Game__acceptable_slides((row, col))
                    for slide in slides:
                        moves.append(((col, row), slide))
                if (
                    self._board[col, row] == self.current_player_idx
                    or self._board[row, col] == -1
                ):
                    slides = self._Game__acceptable_slides((col, row))
                    for slide in slides:
                        moves.append(((row, col), slide))
        return moves

    def play(self, player1: Player, player2: Player) -> int:
        self._board = np.full((5, 5), -1, dtype=np.int8)
        self.current_player_idx = -1
        return super().play(player1, player2)

    # look at the problem of the starting position.
    # The idea could be to leave the play as it is, then we can make our players play as first then as second.
    # we can also make array players shuffle. -> i'll go with this solution
    def train(self, trainee: Player, trainer: Player, epochs: int) -> None:
        players = [trainee, trainer]
        winning_reward = 1
        losing_reward = -1
        bar = tqdm(total=epochs, desc="Epoch")
        for _ in range(epochs):
            np.random.shuffle(players)
            winner_idx = self.play(players[0], players[1])
            if winner_idx != -1:
                if isinstance(players[winner_idx], RLayer):
                    players[winner_idx].back_prop(winning_reward)
                loser_idx = (winner_idx + 1) % 2
                if isinstance(players[loser_idx], RLayer):
                    players[loser_idx].back_prop(losing_reward)
            bar.update(1)
        trainee.save_policy("value_it")


if __name__ == "__main__":
    player = KeyValuePolicyTrainer(is_Q_learn=False)
    g = GameTrainer()
    g.train(player, RandomPlayer(), 100_000)

    wins_as_first = 0
    for _ in range(100):
        winner = g.play(player, RandomPlayer())
        if winner == 0:
            wins_as_first += 1
    print(f"Wins as first: {wins_as_first/100:.2f}%")

    wins_as_second = 0
    for _ in range(100):
        winner = g.play(RandomPlayer(), player)
        if winner == 1:
            wins_as_second += 1
    print(f"Wins as second: {wins_as_second/100:.2f}%")
