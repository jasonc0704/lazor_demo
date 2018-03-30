class Point:
    '''
    The Point.  This object describes the points for which we want the laser
    light to intersect.
    '''

    def __init__(self, pos):
        '''
        Difficulty 1

        DONT FORGET TO COMMENT!
        '''
        self.pos = pos

    def check_intersection(self, pos):
        '''
        A function to check whether the position has been intersected.

        **Parameters**

            pos: *tuple*

        **Returns**

            *Boolean*
        '''
        return self.pos == pos
