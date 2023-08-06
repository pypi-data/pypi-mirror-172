import functools as ft
import time
from collections.abc import Callable


def delay(time_delay: (int, Callable[[], int])):
    """decorator used to delay the decorated function's execution
    :arg time_delay: an integer or callable returning an integer"""
    def dec_delay(func):
        @ft.wraps(func)
        def wrapper(*args, **kwargs):
            wait = time_delay if type(time_delay) == int else time_delay()
            time.sleep(wait)
            func(*args, **kwargs)
        return wrapper
    return dec_delay
