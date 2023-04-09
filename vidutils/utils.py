# Generic utilities
# Module for utilities like execution timers and loggers.

import logging
import time
from functools import wraps


def timed(func):
    """# Timed function decorator
    Use this decorator to wrap a function and return, as last argument, the time elapsed in seconds to execute.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        t1 = time.perf_counter()
        return res, t1 - t0

    return wrapper


def logged(func):
    """# Logged function decorator
    Use this decorator to wrap a function and log each time it is executed.

    TODO add arguments passed to function to the logging.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug(f"called {func.__name__}")
        return func(*args, **kwargs)

    return wrapper
