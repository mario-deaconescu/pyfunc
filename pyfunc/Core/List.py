from typing import TypeVar, Callable
from pyfunc import Option
from pyfunc.Core.Fun import fun1
from pyfunc.Core import Number
from pyfunc.Trace import trace


class Nil[_]:
    pass


class Cons[T](tuple[T, 'Cons[T] | Nil[T]']):
    def __new__(cls, head: T, tail: 't[T]'):
        return super().__new__(cls, (head, tail))


T = TypeVar('T')

t = Nil[T] | Cons[T]


@trace
def map[T, U](list: t[T], f: Callable[[T], U]) -> t[U]:
    match list:
        case Nil():
            return Nil()
        case Cons((head, tail)):
            return Cons(f(head), map(tail, f))


@trace
def iter[T](list: t[T], f: Callable[[T], None]):
    match list:
        case Nil():
            return
        case Cons((head, tail)):
            f(head)
            iter(tail, f)


@trace
def iteri[T](list: t[T], f: Callable[[T, int], None]):
    def helper(list: t[T], f: Callable[[T, int], None], i: int):
        match list:
            case Nil():
                return
            case Cons((head, tail)):
                f(head, i)
                helper(tail, f, i + 1)

    return helper(list, f, 0)


@trace
def foldr[T, U](list: t[T], f: Callable[[U, T], U], initial: U) -> U:
    match list:
        case Nil():
            return initial
        case Cons((head, tail)):
            return f(foldr(tail, f, initial), head)


@trace
def foldl[T, U](list: t[T], f: Callable[[U, T], U], initial: U) -> U:
    match list:
        case Nil():
            return initial
        case Cons((head, tail)):
            return foldl(tail, f, f(initial, head))


@trace
def foldri[T, U](list: t[T], f: Callable[[U, T, int], U], initial: U) -> U:
    def helper(list: t[T], f: Callable[[U, T, int], U], initial: U, i: int) -> U:
        match list:
            case Nil():
                return initial
            case Cons((head, tail)):
                return f(helper(tail, f, initial, i + 1), head, i)

    return helper(list, f, initial, 0)


@trace
def foldli[T, U](list: t[T], f: Callable[[U, T, int], U], initial: U) -> U:
    def helper(list: t[T], f: Callable[[U, T, int], U], initial: U, i: int) -> U:
        match list:
            case Nil():
                return initial
            case Cons((head, tail)):
                return helper(tail, f, f(initial, head, i), i + 1)

    return helper(list, f, initial, 0)


@fun1
@trace
def length[T](list: t[T]) -> int:
    return foldr(list, lambda acc, _: acc + 1, 0)


@trace
def filter[T](list: t[T], f: Callable[[T], bool]) -> t[T]:
    return foldr(list, lambda acc, x: Cons(x, acc) if f(x) else acc, Nil())


@fun1
@trace
def reverse[T](list: t[T]) -> t[T]:
    return foldl(list, lambda acc, x: Cons(x, acc), Nil())


@trace
def append[T](list1: t[T], list2: t[T]) -> t[T]:
    return foldr(list1, lambda acc, x: Cons(x, acc), list2)


@trace
def zip[T, U](list1: t[T], list2: t[U]) -> Option.t[t[tuple[T, U]]]:
    match list1, list2:
        case Cons((head1, tail1)), Cons((head2, tail2)):
            match zip(tail1, tail2):
                case Option.Some(zipped):
                    return Cons((head1, head2), zipped) >> Option.some
                case None:
                    return None
        case Nil(), Nil():
            return Option.Some(Nil())
        case _, _:
            return None


@trace
def equal[T](list1: t[T], list2: t[T]) -> bool:
    match list1, list2:
        case Nil(), Nil():
            return True
        case Cons((head1, tail1)), Cons((head2, tail2)):
            return head1 == head2 and equal(tail1, tail2)
        case _, _:
            return False


@trace
def init[T](n: int, f: Callable[[int], T]) -> t[T]:
    def helper(i: int) -> t[T]:
        if i == n:
            return Nil()
        else:
            return Cons(f(i), helper(i + 1))

    return helper(0)


@trace
def sum[T](list: t[T], to_number: Callable[[T], Number.t]) -> Number.t:
    return foldr(list, lambda acc, x: acc + to_number(x), 0)
