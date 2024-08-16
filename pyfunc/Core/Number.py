from . import Integer, Float
from .Fun import fun1

t = Integer.t | Float.t

@fun1
def to_string(value: t) -> str:
    match value:
        case integer if isinstance(integer, Integer.t):
            return Integer.to_string(integer)
        case float if isinstance(float, Float.t):
            return Float.to_string(float)
        case _:
            raise TypeError(f'Unsupported type: {type(value)}')
