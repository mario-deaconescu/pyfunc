from pyfunc.Core.Fun import curry
from pyfunc.Trace import trace


@trace
def test_curry_sum():
    @curry
    def sum(x: int, y: int, z: int) -> int:
        return x + y + z

    x = sum
