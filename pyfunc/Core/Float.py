from pyfunc.Core import String
from pyfunc.Core.Fun import fun1

t = float


@fun1
def to_string(value: t) -> String.t:
    return str(value)
