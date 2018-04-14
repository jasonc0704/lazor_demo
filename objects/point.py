#!/usr/bin/env python

class Point:
    '''
    The Point. This object describes the points for which we want the laser
    light to intersect.
    '''

    def __init__(self, pos):
        '''
        Creates the point objects.

        **Parameters**

            pos: *tuple*
                A tuple (x, y) representing the coordinates of the point. (Referred as 'position' thereafter)
        '''
        self.pos = pos

    def __repr__(self):
        '''
        Creates a string representation of the point objects.

        **Parameters**

            None

        **Returns**

            repr: *str*
                String representation of the point objects.
        '''
        return 'Point({})'.format(self.pos)

    def check_intersection(self, pos):
        '''
        A function to check whether the position has been intersected.

        **Parameters**

            pos: *tuple*
                This pos is the position of the laser.

        **Returns**

            *Boolean*
        '''
        return self.pos == pos
