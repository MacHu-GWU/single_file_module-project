#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm.timer import *

def test_Timer():
    n = 10000
    l = list(range(n))

    title = "C++ Style for loop"
    # Context Manager Syntax
    with Timer(display=True, title=title) as timer:
        for index in range(n):
            l[index]

    # Objective Oriented
    title = "Python Style for loop"
    timer = Timer(display=True, title=title)
    timer.start()
    for i in l:
        i
    timer.end()


def test_EasyTimer():
    import random

    def sleep_random_time():
        time.sleep(random.randint(100, 1000) / 1000.0)

    timer = EasyTimer()

    timer.start()
    sleep_random_time()
    timer.timeup()

    timer.start()
    sleep_random_time()
    timer.timeup()

    timer.start()
    sleep_random_time()
    timer.timeup()


def test_timeit():
    def func(l):
        for index in range(len(l)):
            item = l[index]

    n = 100
    l = list(range(n))
    kwargs = {"l": l}

    timeit(func, n=10, **kwargs)


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
