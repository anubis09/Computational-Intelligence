import random
from game import Game, Move, Player
import json
from collections import defaultdict


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: "Game") -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class RLayer(Player):
    def __init__(self, path) -> None:
        super().__init__()
        if path:
            f = open(path, "r")
            self._policy = dict(json.load(f))  # metterlo in un default dict
        else:
            self._policy = defaultdict(lambda: dict())

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        # selects the best move in the policy.
        # TODO random moves if none is found
        best_move = None
        board_hash = str(game.get_board())
        best_value = float("-inf")
        for move, value in self._policy[board_hash].items():
            if value > best_value:
                best_move = move
                best_value = value
        return best_move


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
