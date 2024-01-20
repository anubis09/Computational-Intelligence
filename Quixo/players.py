import random
from game import Game, Move, Player
import json
from collections import defaultdict
import os


def random_move() -> tuple[tuple[int, int], Move]:
    from_pos = (random.randint(0, 4), random.randint(0, 4))
    move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
    return from_pos, move


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: "Game") -> tuple[tuple[int, int], Move]:
        return random_move()


class RLayer(Player):
    def __init__(self, name: str = "", file_name: str = "") -> None:
        self.name = name
        self.file_name = file_name
        if file_name:
            path = os.path.join("Quixo", "Policies")
            if not file_name.endswith(".json"):
                file_name = file_name + ".json"
            self.file_name = file_name
            f = open(os.path.join(path, self.file_name), "r")
            print(f"loading {self.file_name}")
            # importing it as a default dict.
            self._policy = defaultdict(lambda: dict(), dict(json.load(f)))
            print(f"{self.file_name} loaded")
        else:
            self._policy = defaultdict(lambda: dict())

    def move_to_str(self, move: tuple[tuple[int, int], Move]) -> str:
        pos, slide = move
        return str(pos) + ";" + str(slide)  # '(1,2);Move.TOP'

    def str_to_move(self, move_str: str) -> tuple[tuple[int, int], Move]:
        pos, slide = move_str.split(";")
        pos = eval(pos)  # from tuple string to just tuple
        slide_move = slide.split(".")[1]  # TOP, BOTTOM, RIGHT, LEFT
        match slide_move:
            case "TOP":
                slide = Move.TOP
            case "LEFT":
                slide = Move.LEFT
            case "BOTTOM":
                slide = Move.BOTTOM
            case _:
                slide = Move.RIGHT
        return (pos, slide)

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        # selects the best move in the policy.
        board_hash = str(game.get_board())
        pl_id = str(game.get_current_player())
        key = board_hash + pl_id
        key.replace(" ", "").replace("[", "").replace("]", "").replace("\n", "")
        # best_move = None
        # best_value = float("-inf")
        # if self._policy[key].keys():
        #     # we know moves in this board set
        #     for k, v in self._policy[key].items():
        #         if v > best_value:
        #             best_value = v
        #             best_move = self.str_to_move(k)
        #     return best_move
        if self._policy[key].keys():
            best_move = self.str_to_move(
                max(self._policy[key].items(), key=lambda item: item[1])[0]
            )
            return best_move
        else:
            # we don't know any moves so we just take one random.
            return random_move()


class HumanPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: "Game") -> tuple[tuple[int, int], Move]:
        print(
            "Remember the convention: X goes left to right, Y goes top to bottom."
        )
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
