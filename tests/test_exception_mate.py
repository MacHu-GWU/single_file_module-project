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


def test_get_last_exc_info():
    try:
        {"a": 1}["b"]
    except Exception as e:
        info = em.get_last_exc_info()
#         print(info)


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
