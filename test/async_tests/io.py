from pyfunc.Trace import trace


@trace
def test_file():
    from pyfunc.Async.Effect import sync, bind
    from pyfunc.Async.IO import open, read
    io = open('test/test.txt', 'r')
    contents = bind(io, read)
    str = sync(contents)
    print(str)
    assert str == 'Line 1\nLine 2\nLine 3\n'


@trace
def test_file_pipe():
    from pyfunc.Async.Effect import sync, map, bind
    from pyfunc.Async.IO import open, read_lines
    from pyfunc.Async import Pipe
    io = open('test/test.txt', 'r')
    pipe = map(io, read_lines)
    lines = bind(pipe, Pipe.to_list)
    list = sync(lines)
    print(list)
    assert list == ['Line 1\n', 'Line 2\n', 'Line 3\n']
