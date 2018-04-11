#!/usr/bin/env python

from functools import wraps
import time


def timer(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = orig_func(*args, **kwargs)
        t1 = time.time()
        print('\n\tTime = %.2f\n' % (t1 - t0))
        return result

    return wrapper
