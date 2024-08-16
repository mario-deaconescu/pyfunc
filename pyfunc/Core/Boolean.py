from pyfunc.Core import String
from pyfunc.Core.Fun import fun1

t = bool


@fun1
def to_string(value: t) -> String.t:
    match value:
        case True:
            return 'true'
        case False:
            return 'false'
