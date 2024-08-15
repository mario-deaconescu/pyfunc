def test_division_error():
    from pyfunc.OrError import try_with, is_error
    result = try_with(lambda: 1 / 0)
    assert is_error(result)


def test_ok():
    from pyfunc.OrError import ok, ok_exn
    result = ok(1)
    assert ok_exn(result) == 1
