#!/usr/bin/env python

import sys
import itertools
import point as pt
import block as blk
import laser as lsr
import time
import copy


class Game:
    '''
    The game grid. Here we read in some user input, assign all our blocks,
    lasers, and points, determine all the possible different combinations
    of boards we could make, and then run through them all to try and find
    the winning one.
    '''

    def __init__(self, fptr):
        '''
        Initialize our game.

        **Parameters**

            fptr: *str*
                The file name of the board to solve.

        **Returns**

            game: *Game*
                This game object.
        '''
        self.fname = fptr
        self.read()

    def read(self):
        '''
        Reads in a file, and generates the point and laser objects.

        **Parameters**

            None

        **Returns**

            content: *list, str*
                The information provided by the input file.
            points_read: *list, Point*
                A list of point objects for a particular board.
            lasers_read: *list, Laser*
                A list of laser objects for a particular board.
        '''
        with open(self.fname, 'r') as infile:
            # First, delete all empty lines in the file.
            content = [line for line in infile.readlines() if line != '\n']

            # Read in the point and laser objects.
            points_read = [pt.Point((int(line.split()[2]), int(line.split()[1])))
                           for line in content if line[0] == 'P']
            lasers_read = [
                lsr.Laser((int(line.split()[2]), int(line.split()[1])), (int(line.split()[4]), int(line.split()[3])))
                for line in content if line[0] == 'L']

        infile.close()

        return content, points_read, lasers_read

    def generate_boards(self):
        '''
        A function to generate all possible board combinations with the
        available blocks.

        **Parameters**

            None

        **Returns**

            boards: *list, Block*
                A list of all possible block arrangements.
        '''

        # Find the grid in the text.
        content = self.read()[0]
        for index, line in enumerate(content):
            if line.upper().startswith('GRID START'):
                grid_start = index
            if line.upper().startswith('GRID STOP'):
                grid_end = index

        # Convert all grid elements to block objects.
        grid = [blk.Block(n) for col in content[grid_start + 1: grid_end] for n in col.split()]

        # Calculate the total space on the board, and the number of rows and columns of the board.
        total_space = len(grid)
        self.board_row = grid_end - grid_start - 1
        self.board_col = total_space / self.board_row

        # Read in movable blocks.
        movable_blocks = [blk.Block(block)
                          for block_read in [line.split()[0] * int(line.split()[1]) for line in content if
                                             (line[0] in ('A', 'B', 'C')) and len(line.split()) == 2]
                          for block in block_read]

        # Read in fixed blocks.
        fixed_blocks = [(block, index) for index, block in enumerate(grid) if block.name in ('A', 'B', 'C', 'x')]

        # Get the positions of all the fixed blocks.
        fixed_pos = [block[1] for block in fixed_blocks]

        # Find all available positions for the movable blocks.
        # Positions of the fixed blocks are excluded.
        available_pos = [pos for pos in range(total_space) if pos not in fixed_pos]

        # Find all combinations of available positions to put in the exact amount of movable blocks.
        # E.g. For a total of 5 available positions and 4 movable blocks, this is 5C4.
        available_pos_combinations = list(itertools.combinations(available_pos, len(movable_blocks)))

        # Calculate permutations for all movable blocks.
        # To ensure the uniqueness of each situation, a set is used.
        movable_block_permutations = {block for block in itertools.permutations(movable_blocks)}

        # Map the movable blocks onto available positions.
        pos_permutations = [zip(block, pos) for block in movable_block_permutations for pos in
                            available_pos_combinations]

        # Generate the potential boards from the permutation results above.
        # Block 'o' is not considered in the permutation calculation, so we initialize the board
        # with this block. Then, for each permutation of the positions, we put blocks (fixed and movable)
        # into their respective positions.
        o = blk.Block('o')
        boards = [[o for count in range(total_space)] for pp in pos_permutations]
        for board, perm in zip(boards, pos_permutations):
            for block, index in perm:
                board[index] = block
                board[index] = block

        return boards

    def set_board(self, board):
        '''
        A function to assign a potential board so that it can be checked.

        **Parameters**

            board: *list, Block*
                A list of block positions.

        **Returns**

            board_to_play: *list, Block*
                A new list of block positions that resembles the coordinate system
                defined for the board. This transformation is done so that the board
                generated can be easily played with. Note, all positions in the list
                are filled with Block objects, including None.
        '''

        # Initialize the board with None blocks.
        none = blk.Block('None')
        board_to_play = [[none for col in range(2 * self.board_col + 1)]
                         for row in range(2 * self.board_row + 1)]

        # Map the blocks from the original board to this new board.
        for b in range(len(board)):
            board_to_play[2 * (b / self.board_col) + 1][2 * (b % self.board_col) + 1] = board[b]

        # Initialize points and lasers before running through each board.
        self.points = self.read()[1]
        self.lasers = self.read()[2]

        return board_to_play

    def save_board(self, board, save_to_file=False):
        '''
        A function to print and save potential boards to file.  This is to be used when
        the solution is found, but can also be used for debugging.

        **Parameters**

            board: *list, Block*
                A list of block positions that is the solution to a particular board.
            save_to_file: *boolean*
                Whether or not save the solution to a txt file. Default=False

        **Returns**

            None
        '''

        # Remove all the None blocks from the board.
        final_board = [[block for block in row if block.name != 'None'] for row in board[1::2]]
        for row in final_board:
            print row

        # The option to save the board to a txt file. Could be turned on manually.
        if save_to_file:
            with open('{}_soln.txt'.format(self.fname.split('.')[0]), 'w') as outfile:
                outfile.write('Solution: \n')
                for row in final_board:
                    outfile.write('{}\n'.format(row))
            outfile.close()

    def run(self):
        '''
        The main code is here.  We call the generate_boards function, then we
        loop through, using set_board to assign a board, "play" the game,
        check if the board is the solution, if so save_board, if not then
        we loop.

        **Returns**

            None
        '''

        # Get all boards
        print('Generating all the boards...')
        sys.stdout.flush()

        boards = self.generate_boards()

        print('Done')
        sys.stdout.flush()

        print("Playing boards...")
        sys.stdout.flush()
        # Loop through the boards, and "play" them
        for board in boards:
            # Set the board
            current_board = self.set_board(board)

            # Start the timing for playing through each board.
            t0 = time.time()

            while self.points != []:
                # If no laser exists (either going outside the boundary
                # or eaten by a B block), then the board fails.
                if self.lasers == []:
                    break

                # Loop through all lasers, and update the board.
                for laser in self.lasers:
                    child_laser = laser.update(current_board, self.points)
                    if child_laser is False:
                        self.lasers.remove(laser)
                    elif child_laser is not None:
                        self.lasers.append(lsr.Laser(child_laser[0], child_laser[1]))

                    # Record the time for the update process of a particular laser.
                    # This is to prevent infinite looping lasers causing by some particular
                    # combinations of A and C blocks.
                    # The time for a laser to loop through the entire board is on the order
                    # of 10^(-5) sec. Here the cutoff is set to 10^(-3) sec. If this limit
                    # is reached, this board fails.
                    t1 = time.time()
                    if t1 - t0 > 0.001:
                        self.lasers = []
                        break

            else:
                # The solution is found!
                print 'Success!'
                break

        # Finally, save the board.
        self.save_board(current_board, save_to_file=False)
