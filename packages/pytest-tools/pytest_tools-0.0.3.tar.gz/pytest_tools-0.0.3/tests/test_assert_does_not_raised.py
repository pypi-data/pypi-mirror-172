import pytest

from pytest_tools import assert_does_not_raise


class TestAssertDoesNotRaised:
    def test_pass_when_no_exception_is_raised(self):
        with assert_does_not_raise():
            pass

    def test_fail_when_an_exception_is_raised(self):
        try:
            with assert_does_not_raise():
                raise Exception()
        except pytest.fail.Exception:
            pass

    def test_returns_an_unexpected_exception_was_raised_as_fail_message_when_an_exception_is_raised(self):
        expected_message = "An unexpected exception Exception was raised"

        try:
            with assert_does_not_raise():
                raise Exception()
        except pytest.fail.Exception as exception:
            assert exception.msg == expected_message
