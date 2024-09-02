import pytest
from async_tests import *
from or_error_tests import *
from list_tests import *
from fun_tests import *
from json_tests import *
from pyfunc.Trace import *


@pytest.fixture(scope='session', autouse=True)
def print_trace():
    with start_tracing('tests') as context:
        try:
            yield
        finally:
            show_context_bars(context)
