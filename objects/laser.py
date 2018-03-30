import block
import point


class Laser:
    '''
    The Laser.  We need to store both the starting position and direction of
    the laser.
    '''

    def __init__(self, pos, dirc):
        '''
        Difficulty 1

        DONT FORGET TO COMMENT!
        '''
        self.pos = pos
        self.dirc = dirc

    def __repr__(self):
        '''

        :return:
        '''
        return 'L %s %s' % (self.pos, self.dirc)

    # MORE
    # Difficulty 4

    @staticmethod
    def reflection_x(dirc):
        '''

        :param dirc:
        :return:
        '''
        x, y = dirc
        return (-x, y)

    @staticmethod
    def reflection_y(dirc):
        '''

        :param dirc:
        :return:
        '''
        x, y = dirc
        return (x, -y)

    def update(self, board, points):
        neighbours = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for neigb in neighbours:
            if board[self.pos[0] + neigb[0]][self.pos[1] + neigb[1]] == block.Block('A') and neigb[0] == 0:
                self.dirc = self.reflection_y(self.dirc)
            if board[self.pos[0] + neigb[0]][self.pos[1] + neigb[1]] == block.Block('A') and neigb[1] == 0:
                self.dirc = self.reflection_x(self.dirc)
            if board[self.pos[0] + neigb[0]][self.pos[1] + neigb[1]] == block.Block('B'):
                self.pos = None
                self.dirc = None
            if board[self.pos[0] + neigb[0]][self.pos[1] + neigb[1]] == block.Block('C') and neigb[0] == 0:
                new_laser = Laser(self.pos, self.dirc)
                self.dirc = self.reflection_y(self.dirc)
            if board[self.pos[0] + neigb[0]][self.pos[1] + neigb[1]] == block.Block('A') and neigb[1] == 0:
                new_laser = Laser(self.pos, self.dirc)
                self.dirc = self.reflection_x(self.dirc)

        return new_laser



pos1 = (2, 7)
dir1 = (1, -1)
pos2 = (4, 5)
dir2 = (-1, -1)
all_lasers = [Laser(pos1, dir1), Laser(pos2, dir2)]
laser1 = all_lasers[0]

if __name__ == '__main__':
    print laser1.dirc

    print laser1.reflection_x((-1, 2))
    print laser1.reflection_y((-1, 2))

