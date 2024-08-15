def test_range():
    from pyfunc.Core import List
    list = List.init(5, lambda x: x ** 2)
    assert List.equal(list, List.Cons(0, List.Cons(1, List.Cons(4, List.Cons(9, List.Cons(16, List.Nil()))))))
