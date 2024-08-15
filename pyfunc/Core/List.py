from typing import TypeVar, Callable
from pyfunc import Option


class Nil[_]:
    pass


class Cons[T](tuple[T, 'Cons[T] | Nil[T]']):
    def __new__(cls, head: T, tail: 't[T]'):
        return super().__new__(cls, (head, tail))


T = TypeVar('T')

t = Nil[T] | Cons[T]


def map[T, U](list: t[T], f: Callable[[T], U]) -> t[U]:
    match list:
        case Nil():
            return Nil()
        case Cons((head, tail)):
            return Cons(f(head), map(tail, f))


def iter[T](list: t[T], f: Callable[[T], None]):
    match list:
        case Nil():
            return
        case Cons((head, tail)):
            f(head)
            iter(tail, f)


def foldr[T, U](list: t[T], f: Callable[[U, T], U], initial: U) -> U:
    match list:
        case Nil():
            return initial
        case Cons((head, tail)):
            return f(foldr(tail, f, initial), head)


def foldl[T, U](list: t[T], f: Callable[[U, T], U], initial: U) -> U:
    match list:
        case Nil():
            return initial
        case Cons((head, tail)):
            return foldl(tail, f, f(initial, head))


def length[T](list: t[T]) -> int:
    return foldr(list, lambda acc, _: acc + 1, 0)


def filter[T](list: t[T], f: Callable[[T], bool]) -> t[T]:
    return foldr(list, lambda acc, x: Cons(x, acc) if f(x) else acc, Nil())


def reverse[T](list: t[T]) -> t[T]:
    return foldl(list, lambda acc, x: Cons(x, acc), Nil())


def append[T](list1: t[T], list2: t[T]) -> t[T]:
    return foldr(list1, Cons, list2)


def zip[T, U](list1: t[T], list2: t[U]) -> Option.t[t[tuple[T, U]]]:
    match list1, list2:
        case Cons((head1, tail1)), Cons((head2, tail2)):
            match zip(tail1, tail2):
                case Option.Some(zipped):
                    return Option.Some(Cons((head1, head2), zipped))
                case None:
                    return None
        case Nil(), Nil():
            return Option.Some(Nil())
        case _, _:
            return None


def equal[T](list1: t[T], list2: t[T]) -> bool:
    match list1, list2:
        case Nil(), Nil():
            return True
        case Cons((head1, tail1)), Cons((head2, tail2)):
            return head1 == head2 and equal(tail1, tail2)
        case _, _:
            return False


def init[T](n: int, f: Callable[[int], T]) -> t[T]:
    def helper(i: int) -> t[T]:
        if i == n:
            return Nil()
        else:
            return Cons(f(i), helper(i + 1))

    return helper(0)
