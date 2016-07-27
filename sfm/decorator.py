#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
collection of usefule decorator.
"""

from __future__ import print_function
import time


def text_of_func_args_and_kwargs(func, args, kwargs):
    """

    **中文文档**

    一个函数的调用以及其参数的文本。
    """
    text_args = ", ".join(["%r" % arg for arg in args])
    text_kwargs = ", ".join(["%s=%r" % (key, value)
                             for key, value in kwargs.items()])
    if text_args and text_kwargs:
        return "%s(%s, %s)" % (func.__name__, text_args, text_kwargs)
    elif (not text_args) and (not text_kwargs):
        return "%s()" % func.__name__
    elif text_args:
        return "%s(%s)" % (func.__name__, text_args)
    elif text_kwargs:
        return "%s(%s)" % (func.__name__, text_kwargs)
    else:
        raise Exception


def timer_wrapper(func):
    """

    **中文文档**

    此包装器可以打印函数的输入参数, 以及运行时间。
    """
    def _wrapper(*args, **kwargs):
        print("Execute: %s" % text_of_func_args_and_kwargs(func, args, kwargs))
        st = time.clock()
        res = func(*args, **kwargs)
        elapsed = time.clock() - st
        print("    Complete! Elapsed %.6f seconds." % elapsed)
        return res

    return _wrapper


#--- Unittest ---
import random


@timer_wrapper
def random_sorted_list(n):
    """Return a random sorted list
    """
    l = [random.randint(1, 1000) for i in range(n)]
    l.sort()
    return l


def test_random_sorted_list():
    n = 1000
    l = random_sorted_list(n)
    print(l)


if __name__ == "__main__":
    test_random_sorted_list()
