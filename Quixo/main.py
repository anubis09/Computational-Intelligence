from game import Game
from players import *

if __name__ == "__main__":
    g = Game()
    player1 = HumanPlayer()
    player2 = RLayer(file_name="policy.json")
    # player1 starts always first.
    winner = g.play(player1, player2)
    print(f"Winner: Player {winner}")
