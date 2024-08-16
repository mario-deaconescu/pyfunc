import json
from typing import Sequence

from pyfunc import OrError
from pyfunc.Core import String, Map, List, Integer, Boolean, Float
from pyfunc.JSON import Object


def parse(json_str: String.t) -> OrError.t[Object.t]:
    def parse_obj(obj) -> OrError.t[Object.t]:
        match obj:
            case Map.t():
                return Map.map(obj, parse_obj) >> OrError.all_map
            case list():
                def parse_list(l: Sequence[object]) -> OrError.t[List.t[Object.t]]:
                    match l:
                        case []:
                            return List.Nil() >> OrError.ok
                        case [head, *tail]:
                            return OrError.bind(parse_obj(head), lambda head:
                            OrError.map(parse_list(tail), lambda tail:
                            List.Cons(head, tail)))
                        case _:
                            return OrError.Error(ValueError(f"Invalid JSON value: {l}"))
                return parse_list(obj)
            case bool():
                return Boolean.t(obj) >> OrError.ok
            case int():
                return Integer.t(obj) >> OrError.ok
            case float():
                return Float.t(obj) >> OrError.ok
            case str():
                return String.t(obj) >> OrError.ok
            case None:
                return OrError.Ok(None)
            case _:
                return OrError.Error(ValueError(f"Invalid JSON value: {obj}"))

    return parse_obj(json.loads(json_str))