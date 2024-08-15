def test_async_simple():
    from pyfunc.Async.Effect import of, map, bind, sync
    effect1 = of(1)
    effect2 = map(effect1, lambda x: x + 1)
    effect3 = bind(effect2, lambda x: of(x + 1))

    assert sync(effect3) == 3


def test_async_after():
    from pyfunc.Async.Effect import after, map, bind, sync
    effect1 = after(0.1, 1)
    effect2 = map(effect1, lambda x: x + 1)
    effect3 = bind(effect2, lambda x: after(0.1, x + 1))
    effect4 = map(effect3, lambda x: x + 1)
    effect5 = bind(effect4, lambda x: after(0.1, x + 1))

    assert sync(effect5) == 5
