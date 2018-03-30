import itertools


def get_partitions(n, k):
    '''
    A robust way of getting all permutations.  Note, this is clearly not the fastest
    way about doing this though.

    **Reference**

     - http://stackoverflow.com/a/34690583
    '''
    for c in itertools.combinations(range(n + k - 1), k - 1):
        yield [b - a - 1 for a, b in zip((-1,) + c, c + (n + k - 1,))]


print(list(get_partitions(6, 17)))
