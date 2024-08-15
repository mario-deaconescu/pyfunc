from pyfunc.Core import String

t = bool


def to_string(value: t) -> String.t:
    match value:
        case True:
            return 'true'
        case False:
            return 'false'
