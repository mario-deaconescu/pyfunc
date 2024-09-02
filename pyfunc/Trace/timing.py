from functools import wraps
from typing import Callable


def timed[T, ** P](func: Callable[P, T]):
    from time import time

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> tuple[T, float]:
        start = time()
        result = func(*args, **kwargs)
        end = time()
        duration = end - start
        return result, duration

    return wrapper


def time[T, ** P](func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> tuple[T, float]:
    return timed(func)(*args, **kwargs)
