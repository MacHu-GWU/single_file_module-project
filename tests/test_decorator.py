# -*- coding: utf-8 -*-

import pytest
from sfm import decorator


def test_elapsed_printer():
    import random

    @decorator.elapsed_printer
    def random_sorted_list(n, lower, upper):
        """Return a random sorted list
        """
        l = [random.randint(lower, upper) for i in range(n)]
        l.sort()
        return l

    n = 1000
    lower = 1
    upper = 9999
    l = random_sorted_list(n, lower=lower, upper=upper)


def test_run_if_is_main():
    assert decorator.test_run_if_is_main() is None


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
