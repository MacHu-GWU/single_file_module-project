#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import time


class Timer(object):
    """A context manager style timer to measure execution time.

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


def timeit(func, n, display=True, title=None, *args, **kwargs):
    """Measure a function's execution time, repeat n times and take the average.

    **中文文档**

    一个测试函数运行时间的小函数, 用于重复运行某函数若干次, 返回运行时间的
    平均值。

    :param func: 待测试的函数
    :param n: 重复的次数
    :param display: 是否打印运行时间
    :param template: 打印信息的模板
    :param args, kwargs: 待测函数的参数

    :returns elapsed: 运行所使用的时间
    """
    template = "elapsed {elapsed:.6f} second, repeat {n} times."
    if title:
        template = title + ": " + template

    st = time.clock()
    for i in range(n):
        func(*args, **kwargs)
    elapsed = (time.clock() - st) / n
    if display:
        print(template.format(elapsed=elapsed, n=n))
    return elapsed
