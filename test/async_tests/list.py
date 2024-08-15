def test_async_list():
    from pyfunc.Async.Effect import after, sync
    from pyfunc.Async.List import map
    from pyfunc.Core import List
    list = List.Cons(1, List.Cons(2, List.Cons(3, List.Nil())))
    list_seq = map(list, lambda x: after(0.1, x + 1), 'sequential')
    list_parallel = map(list, lambda x: after(0.1, x + 1), 'parallel')

    assert List.equal(sync(list_seq), List.Cons(2, List.Cons(3, List.Cons(4, List.Nil()))))
    assert List.equal(sync(list_parallel), List.Cons(2, List.Cons(3, List.Cons(4, List.Nil()))))
