#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import timeit
from sfm.timer import *


def test_Timer():
    n = 1000
    l = list(range(n))

    title = "C++ Style for loop"
    # Context Manager Syntax
    with Timer(display=True, title=title) as timer:
        for index in range(n):
            l[index]
    timer.elapsed

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
    def for_loop(n):
        try:
            range = xrange
        except:
            pass
        for _ in range(n):
            pass

    def for_loop(n):
        for _ in range(n):
            pass

    n = 10 ** 6
    elapsed = timeit.timeit(timeit_wrapper(for_loop, n), number=10)
    # print(elapsed)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
