from pyfunc.Core import List, Map, String, Boolean, Integer
from pyfunc.JSON import Value

t = Value.t | List.t['t'] | Map.t[String.t, 't'] | None


def to_json(obj: t, compact: Boolean.t = False, spaces: Integer.t = 2) -> String.t:
    match compact:
        case True:
            new_line = ' '
            indent_char = ''
        case False:
            new_line = '\n'
            indent_char = ' ' * spaces

    def helper(obj: t, indent: Integer.t) -> String.t:
        indent_str = indent * indent_char
        match obj:
            case None:
                return 'null'
            case value if isinstance(value, Value.t):
                match value:
                    case value if isinstance(value, String.t):
                        return f'"{value}"'
                    case value:
                        return Value.to_json(value)
            case List.Cons((head, tail)):
                extra_indent = (indent + 1) * indent_char
                return (f'[{new_line}'
                        f'{extra_indent}{helper(head, indent + 1)}'
                        f'{List.foldl(tail, initial=str(""),
                                      f=lambda acc, value: f"{acc},{new_line}{extra_indent}{helper(value, indent + 1)}")}'
                        f'{new_line}{indent_str}]{new_line}')
            case Map.t():
                extra_indent = (indent + 1) * indent_char
                match Map.items(obj):
                    case []:
                        return '{}'
                    case List.Cons(((key, value), tail)):
                        return (f'{{{new_line}'
                                f'{extra_indent}"{key}": {helper(value, indent + 1)}'
                                f'{List.foldl(tail, initial=str(""),
                                              f=lambda acc, pair: (f'{acc},{new_line}{extra_indent}"{pair[0]}": '
                                                                   f'{helper(pair[1], indent + 1)}'))}'
                                f'{indent_str}}}')
                    case _:  # unreachable
                        raise ValueError('Map.items(obj) is not a List')
            case _:
                raise TypeError(f'Unsupported type: {type(obj)}')

    return helper(obj, 0)
