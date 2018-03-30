class Block:
    '''
    A generic block for lazor.  We make this extendable so that it can be
    defined as either:

        (a) Reflecting block - Only reflects the laser
        (b) Opaque block - Absorbs the laser
        (c) See-Through block - Both reflects and lets light pass
    '''

    def __init__(self, name):
        '''
        Difficulty 1

        DONT FORGET TO COMMENT!
        '''
        self.name = name
        self.property = {'A':'reflect', 'B': 'absorb', 'C': 'reflect and through', 'o': 'allow', 'x': 'not allow'}

    def __repr__(self):
        '''

        :return:
        '''
        return str(self.name)
