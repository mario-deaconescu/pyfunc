from pyfunc.Core import String
from pyfunc.Core.Fun import fun1
from pyfunc.Trace import trace

t = bool


@fun1
@trace
def to_string(value: t) -> String.t:
    match value:
        case True:
            return 'true'
        case False:
            return 'false'
