from functools import wraps


def timer(orig_func):
    import time

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time()
        print("\n\n\tTime = %.2f" % (t2 - t1))
        return result

    return wrapper

