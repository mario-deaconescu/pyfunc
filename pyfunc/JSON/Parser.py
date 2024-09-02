import json
from typing import Sequence

from pyfunc import OrError
from pyfunc.Core import String, Map, List, Integer, Boolean, Float
from pyfunc.Core.Fun import fun1
from pyfunc.JSON import Object
from pyfunc.Trace import trace


@trace
def parse(json_str: String.t) -> OrError.t[Object.t]:
    @fun1
    @trace
    def parse_obj(obj) -> OrError.t[Object.t]:
        match obj:
            case Map.t():
                return Map.map(obj, parse_obj) >> OrError.all_map
            case list():
                @fun1
                @trace
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

    return json.loads(json_str) >> parse_obj
