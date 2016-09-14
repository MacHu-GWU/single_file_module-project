#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm import rerecipe


def test_extract_by_prefix_surfix():
    assert rerecipe.extract_by_prefix_surfix(
        text="<div>Hello</div><div>World</div>",
        prefix="<div>", surfix="</div>"
    ) == ["Hello", "World"]


def test_extract_number():
    for i, j in zip(
        rerecipe.extract_number(
            "Price is $25.99, age is 18, quarter is .25, one is 1."),
        [25.99, 18, 0.25, 1.0],
    ):
        assert abs(i - j) <= 0.0001


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
