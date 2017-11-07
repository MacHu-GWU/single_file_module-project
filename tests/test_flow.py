#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pytest
from sfm import flow


def bet_and_win(lower=1, upper=100, threshold=50):
    value = random.randint(lower, upper)
    if value > threshold:
        return value
    else:
        raise Exception("%s point, You Lose!" % value)


def test_try_ntime():
    # Successful case
    value = flow.try_ntime(10000, bet_and_win, 1, 10, 5)
    assert value > 5

    # Unsuccessful case
    with pytest.raises(Exception):
        value = flow.try_ntime(1, bet_and_win, 1, 10000, 9999)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
