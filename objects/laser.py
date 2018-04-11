#!/usr/bin/env python

class Laser:
    '''
    The Laser. We need to store both the starting position and direction of
    the laser.
    '''

    def __init__(self, pos, dirc):
        '''
        Creates the laser objects.

        **Parameters**

            pos: *tuple*
                A tuple (x, y) representing the coordinates of the laser. (Referred as 'position' thereafter)
            dirc: *tuple*
                A tuple (x, y) representing the direction of the laser. (Referred as 'direction' thereafter)
                Due to the nature of the game, dirc can only have 4 values, namely
                (1, 1), (1, -1), (-1, 1) and (-1, -1).
        '''
        self.pos = pos
        self.dirc = dirc

    def __repr__(self):
        '''
        Creates a string representation of the laser objects.

        **Parameters**

            None

        **Returns**

            repr: *str*
                String representation of the laser objects.
        '''
        return 'Laser({}, {})'.format(self.pos, self.dirc)

    @staticmethod
    def reflect(dirc, nei):
        '''
        Reflects the direction of the incoming laser according to the position of its neighbour block.
        If the neighbour is above/below the laser, then reflect the direction along y axis.
        If the neighbour is to the left/right of the laser, then reflect the direction along x axis.

        **Parameters**

            dirc: *tuple*
                Direction of the laser.
            nei: *tuple*
                Position of the neighbour block relative to the laser.

        **Returns**

            new_dirc: *tuple*
                The reflected direction.
        '''
        x, y = dirc
        if nei[0] == 0:
            return (x, -y)
        if nei[1] == 0:
            return (-x, y)

    @staticmethod
    def move(pos, dirc):
        '''
        Moves the position of the laser one step along the current direction.

        **Parameters**

            pos: *tuple*
                Position of the laser.
            dirc: *tuple*
                Direction of the laser.

        **Returns**

            new_pos: *tuple*
                New position of the laser after movement.
        '''
        return (pos[0] + dirc[0], pos[1] + dirc[1])

    def update(self, board, points):
        '''
        Updates the board by checking
        (1) all lasers are maintained within the boundary of the board;
        (2) intersection of the laser(s) with the points;
        (3) two neighbours in the forward direction of the lasers
        and acting according to the block types at those positions (if applicable).
        If the laser runs into A, then it is reflected, and nothing is generated;
        if the laser runs into B, then it is absorbed, and thus will be deleted;
        if the laser runs into C, then it passes through, but also generates a child laser whose direction
        is inherits that of the current one.

        **Parameters**

            board: *list, Block*
                The list of block objects representing the board, as generated in game.py
            points: *list*
                A list of tuples for all the positions of the points to be intersected with.

        **Returns**

            child_laser: *tuple* or *boolean: False* or *None*
                New position and direction of the laser after the update.
                If the update indicates a particular board run fails, then returns False.
                If no new laser is generated, then returns None.
        '''

        # Check the intersection of the laser with the points,
        # and deletes the one intersected in the previous step.
        for pt in points:
            if pt.check_intersection(self.pos):
                points.remove(pt)

        # Find the two neighbours along the forward direction of the laser.
        neighbours = [(self.dirc[0], 0), (0, self.dirc[1])]

        for nei in neighbours:
            # First check if the position of the laser is within the boundary of the board.
            # Because of the existence of negative index in lists,
            # it is necessary to ensure that coordinates are all positive.
            try:
                assert self.pos[0] + nei[0] >= 0 and self.pos[1] + nei[1] >= 0
            except AssertionError:
                child_laser = False
                break

            try:
                pos_to_chk = board[self.pos[0] + nei[0]][self.pos[1] + nei[1]].name
            except IndexError:
                child_laser = False
                break

            # Check the block type at the neighbour position and act accordingly.
            if pos_to_chk == 'A':
                child_laser = None
                self.dirc = self.reflect(self.dirc, nei)
                break

            elif pos_to_chk == 'B':
                child_laser = False
                break

            elif pos_to_chk == 'C':
                child_laser = ((self.pos[0] + self.dirc[0], self.pos[1] + self.dirc[1]), self.dirc)
                self.dirc = self.reflect(self.dirc, nei)
                break

            else:
                child_laser = None

        # Move the laser at the end of each step.
        self.pos = self.move(self.pos, self.dirc)

        # Finally, return the result.
        return child_laser
