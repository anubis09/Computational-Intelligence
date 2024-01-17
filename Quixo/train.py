import numpy as np
from game import Game, Move, Player
from players import RLayer, RandomPlayer
import os
import json
from tqdm import tqdm


class KeyValuePolicyTrainer(RLayer):
    def __init__(
        self, is_Q_learn: bool, name: str = "", file_name: str = ""
    ) -> None:
        super().__init__(name, file_name)
        # load policy as default dict.
        self.is_training = True
        self._epsilon = 0.3
        self._game_moves = []
        self._lr = 0.1
        self._gamma_decay = 0.9
        self.is_Q_learn = is_Q_learn

    def set_epsilon(self, eps: int) -> None:
        self._epsilon = eps

    def get_epsilon(self) -> int:
        return self._epsilon

    def exploration(
        self, key: str, possible_moves: list
    ) -> tuple[tuple[int, int], Move]:
        # exploration phase
        index = np.random.choice(len(possible_moves))
        move = possible_moves[index]
        if not move in self._policy[key].keys():
            self._policy[key][self.move_to_str(move)] = 0
        self._game_moves.append((key, self.move_to_str(move)))
        return move

    # def inference(
    #     self, board_hash: str, possible_moves: list
    # ) -> tuple[tuple[int, int], Move]:
    #     best_move = None
    #     best_value = float("-inf")
    #     for move in possible_moves:
    #         if self.move_to_str(move) in self._policy[board_hash].keys():
    #             if (
    #                 self._policy[board_hash][self.move_to_str(move)]
    #                 > best_value
    #             ):
    #                 best_move = move
    #                 best_value = self._policy[board_hash][
    #                     self.move_to_str(move)
    #                 ]
    #         else:
    #             value = 0
    #             if value > best_value:
    #                 best_value = value
    #                 best_move = move

    #     self._policy[board_hash][self.move_to_str(best_move)] = best_value
    #     self._game_moves.append((board_hash, self.move_to_str(best_move)))
    #     return best_move

    # def make_move(self, game: "GameTrainer") -> tuple[tuple[int, int], Move]:
    #     possible_moves = game.get_possible_moves()
    #     board_hash = str(game.get_board())
    #     if self.is_training:
    #         if np.random.random() < self._epsilon:
    #             move = self.exploration(
    #                 board_hash=board_hash, possible_moves=possible_moves
    #             )
    #             return move
    #         else:
    #             return self.inference(board_hash, possible_moves)
    #     else:
    #         return self.inference(board_hash, possible_moves)

    def make_move(self, game: "GameTrainer") -> tuple[tuple[int, int], Move]:
        possible_moves = game.get_possible_moves()
        board_hash = str(game.get_board())
        pl_id = str(game.get_current_player())
        key = board_hash + pl_id
        if self.is_training and np.random.random() < self._epsilon:
            move = self.exploration(key=key, possible_moves=possible_moves)
            return move
        else:
            # best_move = None
            # best_value = float("-inf")
            # if self._policy[key].keys():
            #     # we know moves in this board set
            #     for k, v in self._policy[key].items():
            #         if v > best_value:
            #             best_value = v
            #             best_move = self.str_to_move(k)
            if self._policy[key].keys():
                best_move = self.str_to_move(
                    max(self._policy[key].items(), key=lambda item: item[1])[0]
                )
                self._game_moves.append((key, self.move_to_str(best_move)))
                return best_move
            else:
                # we don't know any moves so we just take it randomly.
                move = self.exploration(key=key, possible_moves=possible_moves)
                return move

    # def make_move(self, game: "GameTrainer") -> tuple[tuple[int, int], Move]:
    #     possible_moves = game.get_possible_moves()
    #     board_hash = str(game.get_board())
    #     if np.random.random() < self._epsilon:
    #         move = self.exploration(
    #             board_hash=board_hash, possible_moves=possible_moves
    #         )
    #         return move
    #     else:
    #         # selects the best move in the policy.
    #         best_move = None
    #         best_value = float("-inf")
    #         for move in possible_moves:
    #             if self.move_to_str(move) in self._policy[board_hash].keys():
    #                 if (
    #                     self._policy[board_hash][self.move_to_str(move)]
    #                     > best_value
    #                 ):
    #                     best_move = move
    #                     best_value = self._policy[board_hash][
    #                         self.move_to_str(move)
    #                     ]
    #             else:
    #                 value = 0
    #                 if value > best_value:
    #                     best_value = value
    #                     best_move = move

    #         self._policy[board_hash][self.move_to_str(best_move)] = best_value
    #         self._game_moves.append((board_hash, self.move_to_str(best_move)))
    #         return best_move
    # best_move = None
    # best_value = float("-inf")
    # if self._policy[board_hash].keys():
    #     # we know moves in this board set
    #     for k, v in self._policy[board_hash].items():
    #         if v > best_value:
    #             best_value = v
    #             best_move = self.str_to_move(k)
    #     self._game_moves.append(
    #         (board_hash, self.move_to_str(best_move))
    #     )
    #     return best_move
    # else:
    #     # we don't know any moves so we just take it randomly.
    #     move = self.exploration(
    #         board_hash=board_hash, possible_moves=possible_moves
    #     )
    #     return move

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
        return counter, len(self._policy.keys())

    def save_policy(self) -> None:
        """
        It saves the policy
        """
        path = os.path.join("Quixo", "Policies")
        if not os.path.exists(path):
            os.makedirs(path)
        if not self.file_name:
            self.file_name = "new_policy_value_it_" + self.name + ".json"
        f = open(os.path.join(path, self.file_name), "w")
        print(f"saving {self.file_name}")
        json.dump(self._policy, f, indent=4)
        print(f"{self.file_name} saved")


class GameTrainer(Game):
    def __init__(self) -> None:
        super().__init__()

    def print(self) -> None:
        # os.system("cls||clear")
        pass

    def __acceptable_slides(self, from_position: tuple[int, int]):
        """When taking a piece from {from_position} returns the possible moves (slides)"""
        acceptable_slides = [Move.BOTTOM, Move.TOP, Move.LEFT, Move.RIGHT]
        axis_0 = from_position[0]  # axis_0 = 0 means uppermost row
        axis_1 = from_position[1]  # axis_1 = 0 means leftmost column

        if axis_0 == 0:  # can't move upwards if in the top row...
            acceptable_slides.remove(Move.TOP)
        elif axis_0 == 4:
            acceptable_slides.remove(Move.BOTTOM)

        if axis_1 == 0:
            acceptable_slides.remove(Move.LEFT)
        elif axis_1 == 4:
            acceptable_slides.remove(Move.RIGHT)
        return acceptable_slides

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
                    slides = self.__acceptable_slides((row, col))
                    for slide in slides:
                        moves.append(((col, row), slide))
                if (
                    self._board[col, row] == self.current_player_idx
                    or self._board[col, row] == -1
                ):
                    slides = self.__acceptable_slides((col, row))
                    for slide in slides:
                        moves.append(((row, col), slide))
        return moves

    def play(self, player1: Player, player2: Player) -> int:
        self._board = np.full((5, 5), -1, dtype=np.int8)
        self.current_player_idx = -1
        players = [player1, player2]
        winner = -3
        n_move = 0
        while winner < 0 and n_move < 150:
            self.current_player_idx += 1
            self.current_player_idx %= len(players)
            ok = False
            in_loop = 0
            while not ok:
                in_loop += 1
                from_pos, slide = players[self.current_player_idx].make_move(
                    self
                )
                ok = self._Game__move(from_pos, slide, self.current_player_idx)
                if in_loop > 200:
                    pass
            n_move += 1
            winner = self.check_winner()
        return winner

    # look at the problem of the starting position.
    # The idea could be to leave the play as it is, then we can make our players play as first then as second.
    # we can also make array players shuffle. -> i'll go with this solution
    def train(self, trainee: Player, trainer: Player, epochs: int) -> None:
        if not trainee.file_name:
            trainee.set_epsilon(1)
        if not trainer.file_name:
            trainer.set_epsilon(1)
        players = [trainee, trainer]
        winning_reward = 1
        losing_reward = -3
        first_draw_reward = 0.1
        second_draw_reward = 0.5
        bar = tqdm(total=epochs, desc="Epoch")
        for ep in range(epochs):
            if ep % (epochs // 100) == 0:
                old_eps = trainee.get_epsilon()
                new_eps = old_eps - 0.1 if old_eps > 0.3 else old_eps
                # eps decrease at the same rate for both.
                trainee.set_epsilon(new_eps)
                trainer.set_epsilon(new_eps)
            np.random.shuffle(players)
            winner_idx = self.play(players[0], players[1])
            loser_idx = (winner_idx + 1) % 2
            if winner_idx != -1:
                if isinstance(players[winner_idx], RLayer):
                    players[winner_idx].back_prop(winning_reward)
                if isinstance(players[loser_idx], RLayer):
                    players[loser_idx].back_prop(losing_reward)
            else:
                if isinstance(players[0], RLayer):
                    # if first start draws, not very good.
                    players[0].back_prop(first_draw_reward)
                if isinstance(players[1], RLayer):
                    # if second starting draws, good for him
                    players[1].back_prop(second_draw_reward)
            bar.update(1)
        if isinstance(trainee, RLayer):
            trainee.save_policy()
        if isinstance(trainer, RLayer):
            trainer.save_policy()
        return


if __name__ == "__main__":
    player_trainee = KeyValuePolicyTrainer(
        is_Q_learn=False,
        name="trainee",
        file_name="new_policy_value_it_trainee_600m.json",
    )
    player_trainer = KeyValuePolicyTrainer(
        is_Q_learn=False,
        name="trainer",
        file_name="new_policy_value_it_trainer_600m.json",
    )
    g = GameTrainer()
    g.train(player_trainee, player_trainer, 100_000)

    player_trainee.is_training = False
    n_game = 5000

    print("starting evaluation as first player")
    wins_as_first = 0
    for _ in range(n_game):
        winner = g.play(player_trainee, RandomPlayer())
        if winner == 0:
            wins_as_first += 1
    print(f"Wins as first: {wins_as_first/n_game:.2f}%")

    print("starting evaluation as second player")
    wins_as_second = 0
    for _ in range(n_game):
        winner = g.play(RandomPlayer(), player_trainee)
        if winner == 1:
            wins_as_second += 1
    print(f"Wins as second: {wins_as_second/n_game:.2f}%")
