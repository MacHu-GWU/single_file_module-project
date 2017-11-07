#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm import string_match


def test_choose_best():

    choice = [
        "Atlanta Falcons",
        "New Cow Jets",
        "Tom boy",
        "New York Giants",
        "Dallas Cowboys",
    ]
    text = "cowboy"
    res = string_match.choose_best(text, choice)
    print(res)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
