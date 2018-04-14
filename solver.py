#!/usr/bin/env python

'''
The main call to the Lazor code. This will load up the
game object, initialized by a board, and then run the game!
'''

import os
import time
import timer
from objects.game import Game


@timer.timer
def solve(fptr):
    # Start the game
    g = Game(fptr)
    print 'Solving the board {}'.format(fptr)
    # Solve the board
    g.run()

# Run and time
if __name__ == "__main__":
    t0 = time.time()
    os.chdir('boards')
    solve('braid_5.input')
    solve('diagonal_8.input')
    solve('diagonal_9.input')
    solve('mad_1.input')
    solve('mad_7.input')
    solve('showstopper_2.input')
    solve('tricky_1.input')
    solve('vertices_1.input')
    solve('vertices_2.input')
    t = time.time() - t0
    print 'Total Time = %.2f' % t
