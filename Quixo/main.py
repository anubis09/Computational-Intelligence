from Quixo.old_game import Game
from players import *

if __name__ == "__main__":
    g = Game()
    player1 = HumanPlayer()
    player2 = RandomPlayer()
    # player1 starts always first.
    winner = g.play(player2, player1)
    print(f"Winner: Player {winner}")
