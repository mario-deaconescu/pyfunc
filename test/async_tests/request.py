from pyfunc.Trace import trace


@trace
def test_http_get():
    from pyfunc.Async.Effect import sync
    from pyfunc.Async.Request import create_client, get, close
    client = sync(create_client())
    text = sync(get(client, 'https://httpbin.org/get'))
    assert 'httpbin.org' in text
    sync(close(client))
    assert True
