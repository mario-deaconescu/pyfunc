from pyfunc.Core import Number, String, Boolean, Integer

t = Number.t | String.t | Boolean.t


def to_json(value: t) -> str:
    match value:
        case boolean if isinstance(boolean, Boolean.t):
            return Boolean.to_string(boolean)
        case number if isinstance(number, Number.t):
            return Number.to_string(number)
        case string if isinstance(string, String.t):
            return string
        case _:
            raise TypeError(f'Unsupported type: {type(value)}')
