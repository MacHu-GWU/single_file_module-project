#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm import exception_mate as em


def test_Exception():
    e = Exception()
    assert str(e) == ""

    e = Exception("something wrong!")
    assert str(e) == "something wrong!"

    e = Exception("args1", "args2")
    assert str(e) == "('args1', 'args2')"


def test_ExceptionHavingDefaultMessage():
    class InputError(em.ExceptionHavingDefaultMessage):
        default_message = "array cannot be empty!"

    e = InputError()
    assert str(e) == "array cannot be empty!"

    e = InputError("array cannot be all None!")
    assert str(e) == "array cannot be all None!"

    e = InputError("args1", "args2")
    assert str(e) == "('args1', 'args2')"

    class OutputError(em.ExceptionHavingDefaultMessage):
        pass

    e = OutputError()
    with pytest.raises(NotImplementedError):
        str(e)


def test_ErrorTraceBackChain():
    def inner():
        raise ValueError("inner exception")

    def outer():
        inner()

    try:
        outer()
    except:
        etbc = em.ErrorTraceBackChain.get_last_exc_info()
        assert len(etbc) == 3

        assert etbc.raised_error.exc_type == ValueError
        assert etbc.raised_error.func_name == "test_ErrorTraceBackChain"
        assert etbc.raised_error.code == "outer()"

        assert etbc.source_error.exc_type == ValueError
        assert etbc.source_error.func_name == "inner"
        assert etbc.source_error.code == 'raise ValueError("inner exception")'
        import traceback


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
