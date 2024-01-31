import numpy as np
from game import Game, Move, Player
from players import RLayer, RandomPlayer
import os
import json
import heapq
from tqdm import tqdm


class KeyValuePolicyTrainer(RLayer):
    def __init__(self, name: str = "", file_name: str = "") -> None:
        super().__init__(name, file_name)
        # load policy as default dict.
        self.is_training = True
        self._epsilon = 0.3
        self._game_moves = []
        self._lr = 0.2
        self._gamma_decay = 0.9

    def set_epsilon(self, eps: int) -> None:
        """Set the exploration rate."""
        self._epsilon = eps

    def get_epsilon(self) -> int:
        """Returns the current exploration rate."""
        return self._epsilon

    def exploration(
        self, key: str, possible_moves: list
    ) -> tuple[tuple[int, int], Move]:
        """Returns a random move from all the possible ones."""
        index = np.random.choice(len(possible_moves))
        move = possible_moves[index]
        if not move in self._policy[key].keys():
            self._policy[key][self.move_to_str(move)] = 0
        self._game_moves.append((key, self.move_to_str(move)))
        return move

    def make_move(self, game: "GameTrainer") -> tuple[tuple[int, int], Move]:
        """Returns a random move if goes in exploration, otherwise returns the best move that the agent has learnt."""
        possible_moves = game.get_possible_moves()
        board_hash = str(game.get_board())
        pl_id = str(game.get_current_player())
        key = board_hash + pl_id
        # remove not useful characters.
        key = (
            key.replace(" ", "")
            .replace("[", "")
            .replace("]", "")
            .replace("\n", "")
        )
        if self.is_training and np.random.random() < self._epsilon:
            # exploration mode.
            move = self.exploration(key=key, possible_moves=possible_moves)
            return move
        else:
            # we take the best move for this state from our policy
            if self._policy[key].keys():
                best_move = self.str_to_move(
                    max(self._policy[key].items(), key=lambda item: item[1])[0]
                )
                self._game_moves.append((key, self.move_to_str(best_move)))
                return best_move
            else:
                # we've never seen the state, so we go in exploration
                move = self.exploration(key=key, possible_moves=possible_moves)
                return move

    def back_prop(self, reward: int) -> None:
        """
        The back_prop function is responsible for updating the policy values in the agent's memory during the training process.
        It adjusts the policy values based on the received reward.
        """
        for _ in range(len(self._game_moves)):
            state = self._game_moves.pop()
            # state is a tuple(board, move)
            board = state[0]
            move = state[1]
            self._policy[board][move] += self._lr * (
                self._gamma_decay * reward - self._policy[board][move]
            )
            reward = self._policy[board][move]
        # the game is ended, so we reset the move list.
        self._game_moves = []
        return

    def save_space(self, top_k: int = -1) -> None:
        """Shrinks the policy, without impatting the performances."""
        MIN_MOVES = 4
        N_DECIMAL = 2

        print("started pruning")
        for k, dictio in list(self._policy.items()):
            all_sub_keys = list(dictio.keys())
            # we remove all states that are associated with less moves than MIN_MOVES.
            if len(all_sub_keys) <= MIN_MOVES:
                self._policy.pop(k)
            elif len(all_sub_keys) >= top_k > 0:
                # We select the top_k keys
                k_keys = heapq.nlargest(
                    top_k, dictio, key=dictio.get
                )  # this sort by values.
                for sub_key in all_sub_keys:
                    # we remove all the keys that are not in the top_k list.
                    if sub_key not in k_keys:
                        dictio.pop(sub_key)
                    else:
                        if top_k == 1:
                            new_val = round(dictio[sub_key], N_DECIMAL)
                            # if the rounded value is really low, we can prune those states.
                            if new_val <= 0.01:
                                self._policy.pop(k)
                            else:
                                dictio[sub_key] = new_val

        print("pruning ended")
        return

    def save_policy(self) -> None:
        """This function saves the policy in a JSON file."""
        path = os.path.join("Quixo", "Policies")
        if not os.path.exists(path):
            os.makedirs(path)
        if not self.file_name:
            self.file_name = "new_policy_value_it_" + self.name + ".json"
        f = open(os.path.join(path, self.file_name), "w")
        print(f"saving {self.file_name}")
        json.dump(self._policy, f)
        print(f"{self.file_name} saved")
        return


class GameTrainer(Game):
    def __init__(self) -> None:
        super().__init__()

    def print(self) -> None:
        # we need to train, so we don't need to print the board states.
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

    def get_possible_moves(self) -> list[tuple[tuple[int, int], Move]]:
        """This function returns all the possible moves valid in the current board state"""
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
        """Same play of the parent class, but we reset the board, and we count the number of moves made."""
        self._board = np.full((5, 5), -1, dtype=np.int8)
        self.current_player_idx = -1
        players = [player1, player2]
        winner = -3
        n_move = 0
        while winner < 0 and n_move < 150:
            self.current_player_idx += 1
            self.current_player_idx %= len(players)
            ok = False
            while not ok:
                from_pos, slide = players[self.current_player_idx].make_move(
                    self
                )
                ok = self._Game__move(from_pos, slide, self.current_player_idx)
            n_move += 1
            winner = self.check_winner()
        return winner

    def train(self, trainee: Player, trainer: Player, epochs: int) -> None:
        """Function for training two agents at the same time."""
        if not trainee.file_name:
            # First training, so we start with full exploration mode.
            print("starting full exploration mode")
            trainee.set_epsilon(1)
        if isinstance(trainer, RLayer) and not trainer.file_name:
            trainer.set_epsilon(1)
        players = [trainee, trainer]
        winning_reward = 1
        losing_reward = -3
        first_draw_reward = 0.1
        second_draw_reward = 0.5
        bar = tqdm(total=epochs, desc="Epoch")
        for ep in range(epochs):
            if ep % (epochs // 30) == 0:
                # step by step we reduce the exporation rate.
                old_eps = trainee.get_epsilon()
                new_eps = old_eps - 0.1 if old_eps > 0.3 else old_eps
                trainee.set_epsilon(new_eps)
                # eps decrease at the same rate for both.
                if isinstance(trainer, RLayer):
                    trainer.set_epsilon(new_eps)
            # we shuffle the players so the agent is trained to start as first and as second.
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
        # we can also save the policy learned from the trainer.
        # if isinstance(trainer, RLayer):
        #     trainer.save_policy()
        return


if __name__ == "__main__":
    player_trainee = KeyValuePolicyTrainer(
        name="",
        file_name="policy.json",
    )

    g = GameTrainer()

    # g.train(player_trainee, RandomPlayer(), 2_000)

    player_trainee.is_training = False
    n_game = 2000

    print("starting evaluation as first player")
    wins_as_first = 0
    for _ in range(n_game):
        winner = g.play(player_trainee, RandomPlayer())
        if winner == 0:
            wins_as_first += 1
    print(f"Wins as first: {wins_as_first/n_game:.2%}")

    print("starting evaluation as second player")
    wins_as_second = 0
    for _ in range(n_game):
        winner = g.play(RandomPlayer(), player_trainee)
        if winner == 1:
            wins_as_second += 1
    print(f"Wins as second: {wins_as_second/n_game:.2%}")

    print(
        f"total percentage: {(wins_as_first + wins_as_second)/(n_game*2):.2%}"
    )

    player_trainee.policy_stat()

    # please if you want to use save space on the loaded policy, change N_MOVES to 0.
    # player_trainee.save_space(1)

    player_trainee.policy_stat()

    player_trainee.save_policy()
