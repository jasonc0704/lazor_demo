import sys
import copy
import itertools
import os
import point as pt
import block as blk
import laser as lsr


# import the Point, Block, and Laser objects


class Game:
	'''
	The game grid.  Here we read in some user input, assign all our blocks,
	lasers, and points, determine all the possible different combinations
	of boards we could make, and then run through them all to try and find
	the winning one.
	'''

	def __init__(self, fptr):
		'''
		Difficulty 1

		Initialize our game.

		**Parameters**

			fptr: *str*
				The file name of the input board to solve.

		**Returns**

			game: *Game*
				This game object.
		'''
		self.fname = fptr
		self.read()

	# DO SOMETHING HERE SO WE CAN PRINT A REPRESENTATION OF GAME!

	def read(self):
		'''
		Difficulty 3

		Some function that reads in a file, and generates the internal board.

		**Parameters**

			fptr: *str*
				The file name of the input board to solve.

		**Returns**

			self.blocks, self_available_space: *tuple*
											 The list representation of the initial board to be used.
		'''
		os.chdir('../boards')
		with open(self.fname, 'r') as fptr:
			# Find a representation of the board.
			content = fptr.readlines()
			grid_start = ''.join(line for line in content if line.startswith('GRID START'))
			grid_end = ''.join(line for line in content if line.startswith('GRID STOP'))
			grid = [blk.Block(n) for col in content[content.index(grid_start) + 1: content.index(grid_end)] for n in
					col.split()]
			self.grid = grid
			self.grid_row = content.index(grid_end) - content.index(grid_start) - 1
			self.grid_col = grid.__len__() / self.grid_row
			print 'grid has %s col' % self.grid_col

			self.blocks = [line.split()[0] * int(line.split()[1]) for line in content if
						   (line.startswith('A') or line.startswith('B') or line.startswith('C')) and len(
							   line.split()) == 2]

			self.blocks = [blk.Block(block) for _type in self.blocks for block in _type]

			self.fixed_blocks = [(block, index) for index, block in enumerate(grid) if block.name in ('A', 'B', 'C', 'x')]

			self.available_space = grid.__len__() - self.fixed_blocks.__len__()

			self.points = [(int(line.split()[2]), int(line.split()[1])) for line in content if line.startswith('P')]
			self.lasers = [
				lsr.Laser((int(line.split()[2]), int(line.split()[1])), (int(line.split()[4]), int(line.split()[3]))) for
				line in content if line.startswith('L')]

			print(grid)
			print(self.fixed_blocks)
			print('Blocks are %s' % (self.blocks))
			print len(self.blocks)
			print('Number of available space: %s ' % self.available_space)
			print('Points are %s' % (self.points))
			print('Lasers are %s' % (self.lasers))

		fptr.close()

		# return self.blocks, self.available_space

	def generate_boards(self):
		'''
		Difficulty 3
		
		A function to generate all possible board combinations with the
		available blocks.

		First get all possible combinations of blocks on the board (we'll call these boards)
		  We know we have self.blocks, and N_blocks = len(self.blocks)
		  We also know we have self.available_space
		  So, essentially we have to find all the possible ways to put N_blocks into
		  self.available_space
		This becomes the "stars and bars" problem; however, we have distinguishable "stars",
		and further we restrict our system so that only one thing can be put in each bin.

		**Returns**

			None
		'''
		block_permutation = []
		permutation = list(itertools.permutations(self.blocks,self.blocks.__len__()))
		# print permutation
		bp_s = []
		for p in permutation:
			if str(p) not in bp_s:
				bp_s.append(str(p))
				block_permutation.append(p)

		fixed_place = [place[1] for place in self.fixed_blocks]
		a = range(self.grid.__len__())
		for i in fixed_place:
			a.remove(i)
		places = list(itertools.combinations(a, self.blocks.__len__()))

		all_permutations = [zip(bp, pl) for bp in block_permutation for pl in places]

		all_boards = []

		for per in all_permutations:
			board = [[None for col in range(2 * self.grid_col + 1)] for row in range(2 * self.grid_row + 1)]

			for i, j in per:
				board[2 * (j / self.grid_col) + 1][2 * (j % self.grid_col) + 1] = i

			all_boards.append(board)

		final_boards = []
		for board in all_boards:
			for i, j in self.fixed_blocks:
				board[2 * (j / self.grid_col) + 1][2 * (j % self.grid_col) + 1] = i

			final_boards.append(board)

		print '1st'
		for line in final_boards[0]:
			print line

		print 'last'
		for line in final_boards[-1]:
			print line



	def set_board(self, board):
		'''
		Difficulty 2

		A function to assign a potential board so that it can be checked.

		**Parameters**

			board: *list, Block*
				A list of block positions.  Note, this list is filled with
				None, unless a block is at said position, then it is a
				Block object.

		**Returns**

			None
		'''
		# YOUR CODE HERE
		pass

	def save_board(self):
		'''
		Difficulty 2

		A function to save potential boards to file.  This is to be used when
		the solution is found, but can also be used for debugging.

		**Returns**

			None
		'''



def run(self):
	'''
	Difficulty 3

	The main code is here.  We call the generate_boards function, then we
	loop through, using set_board to assign a board, "play" the game,
	check if the board is the solution, if so save_board, if not then
	we loop.

	**Returns**

		None
	'''

	# Get all boards
	print("Generating all the boards..."),
	sys.stdout.flush()
	boards = self.generate_boards()
	print("Done")
	sys.stdout.flush()

	print("Playing boards...")
	sys.stdout.flush()
	# Loop through the boards, and "play" them
	for b_index, board in enumerate(boards):
		# Set board
		self.set_board(board)

		# MAYBE MORE CODE HERE?
		current_lasers = [lsr.Laser(laser) for laser in self.lasers]

		# LOOP THROUGH LASERS
		# for j, laser in enumerate(current_lasers):
		#     child_laser = None
		#     child_laser = laser.update(self.board, self.points)

		# MAYBE MORE CODE HERE?

		# CHECKS HERE
		points = [pt.Point(point).pos for point in self.points]
		for laser in current_lasers:
			new_laser = laser.update(board, points)
			if new_laser is not None:
				current_lasers.append(new_laser)


g = Game('diagonal_9.input')
g.generate_boards()
# g.save_board()
