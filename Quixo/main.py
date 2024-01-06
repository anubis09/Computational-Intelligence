import random
from game import Game, Move, Player
from collections import defaultdict


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
        self.epsilon = 0.3
        self.lr = 0.1
        self.gamma_decay = 0.9
        self.q_table = defaultdict(float)

    # Come possiamo salvare uno stato?
    # visto che la mossa move non può essere fatta, possiamo salvare come key nel dictionary:
    # tuple(state, movetodo) e poi assegnare un valore.

    # Aspetti critici: Le mosse vengono checkate nella funzione play in cui c'è un while.
    # Questo vuol dire che serve un controllo per vedere se la mossa è valida oppure no.
    # Tipo di controllo: quando ricevi uno stato controllare di non avere già una mossa con quello stato salvata nelle done moves.
    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        return super().make_move(game)


class HumanPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: "Game") -> tuple[tuple[int, int], Move]:
        print(
            "Remember the convention: X goes left to right, Y goes top to bottom. "
        )
        inp = input("insert the X and Y coordinate in the format: 'x y': ")
        x, y = (int(coord) for coord in inp.split(" "))
        move = input("insert the slide move (TOP,LEFT,BOTTOM,RIGHT): ")
        match move.upper:
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


if __name__ == "__main__":
    g = Game()
    player1 = HumanPlayer()
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    print(f"Winner: Player {winner}")
