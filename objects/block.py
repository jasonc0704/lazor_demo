#!/usr/bin/env python

class Block:
    '''
    A generic block for lazor.  We make this extendable so that it can be
    defined as either:
        (A) Reflecting block - Only reflects the laser
        (B) Opaque block - Absorbs the laser
        (C) See-Through block - Both reflects and lets light pass
    '''

    def __init__(self, name):
        '''
        Creates the block objects.

        **Parameters**

            name: *str*
                The name of the block object, also serving as its type defined above.
        '''
        self.name = name

    def __repr__(self):
        '''
        Creates a string representation of the block objects.

        **Parameters**

            None

        **Returns**

            repr: *str*
                String representation of the block objects.
        '''
        return '{}'.format(self.name)

    def __eq__(self, other):
        '''
        Defines equality of two block objects.

        **Parameters**

            other: *Block*
                The block object to compare with.

        **Returns**

            *boolean*
                Checks whether two block objects have the same name.
        '''
        return self.name == other.name

    def __hash__(self):
        '''
        Defines the hash function for the block class.

        **Returns**

            hash: *int*
                The hash value of the name of the block objects.
        '''
        return hash(self.name)
