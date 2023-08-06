from contextlib import contextmanager

import pytest


def get_exception_name(exception):
    return type(exception).__name__


def get_fail_message(exception):
    return f"An unexpected exception {get_exception_name(exception)} was raised"


@contextmanager
def assert_does_not_raise():
    try:
        yield
    except Exception as exception:
        pytest.fail(get_fail_message(exception))