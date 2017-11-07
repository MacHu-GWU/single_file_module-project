#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lazy time profiling tools.
"""

from __future__ import print_function
import time


class Timer(object):
    """
    A context manager style timer to measure execution time.

    **中文文档**

    一个简单的计时器, 提供了Context Manager语法。

    Example1::

        # Context Manager
        n = 1000 * 1000
        l = list(range(n))

        title = "C++ Style for loop"
        # Context Manager Syntax
        with Timer(title, display=True) as timer:
            for index in range(n):
                l[index]

    请注意, 该Timer的实现方式仅仅是用两个time.clock()相减, 效果并不会太好。
    """

    def __init__(self, display=True, title=None):
        self._start = None
        self._end = None
        self._elapsed = None
        self._display = display
        self._template = "elapsed {elapsed:.6f} second."
        self._title = title
        if title:
            self._template = title + ": " + self._template

    def start(self):
        self._start = time.clock()

    def end(self):
        self._end = time.clock()
        self._elapsed = self._end - self._start
        if self._display:
            self.display()

    def display(self):
        print(self._template.format(elapsed=self._elapsed))

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc_info):
        self.end()

    @property
    def elapsed(self):
        return self._elapsed


class EasyTimer(object):
    """A Timer can measure execution time of multiple block of time, respectively.
    """

    def __init__(self):
        self.st = None
        self.ed = None
        self.elapsed = None
        self.records = list()

    @property
    def total_elapsed(self):
        return sum(self.records)

    # single time, multiple time measurement
    def start(self):
        """Start measuring.
        """
        self.st = time.clock()

    def stop(self):
        """Save last elapse time to self.records.
        """
        self.ed = time.clock()
        self.elapsed = self.ed - self.st
        self.records.append(self.elapsed)

    def timeup(self):
        """Print the last measurement elapse time, and return it.
        """
        self.stop()
        self.display()

    def click(self):
        """Record the last elapse time and start the next measurement.
        """
        self.stop()
        self.start()

    def display(self):
        """Print the last elapse time.
        """
        print("Elapsed %.6f seconds" % self.elapsed)

    def reset(self):
        """Reset the timer.
        """
        self.elapsed = 0.0
        self.records = list()


def timeit_wrapper(func, *args, **kwargs):
    """
    Wrapper function makes ``timeit.timeit`` easier to use.

    Usage::

        >>> import timeit
        >>> def func(*args, **kwargs): pass
        >>> timeit.timeit(timeit_wrapper(func, *args, **kwargs), number=10)
        0.000153
    """
    def wrapper():
        return func(*args, **kwargs)
    return wrapper
