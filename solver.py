'''
The main call to the Lazor code.  This will load up the
game object, initialized by a board, and then run the game!
'''

import time
from objects.game import Game
import timer


@timer.timer
def solve(fptr):
    # Start the game
    g = Game(fptr)
    # Print a representation of the board
    print(g)
    # Solve the board, and time how long it took.
    g.run()


if __name__ == "__main__":
    solve("mad_1.input")
