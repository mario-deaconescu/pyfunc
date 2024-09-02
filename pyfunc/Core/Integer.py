from pyfunc.Core import String
from pyfunc.Core.Fun import fun1
from pyfunc.Trace import trace

t = int


@fun1
@trace
def to_string(value: t) -> String.t:
    return str(value)
