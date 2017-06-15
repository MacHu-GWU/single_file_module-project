#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm import rerecipe


def test_extract_by_prefix_surfix():
    text = "<div>Hello</div><div>World</div>"

    assert rerecipe.extract_by_prefix_surfix(
        text=text,
        prefix="<div>", surfix="</div>",
    ) == ["Hello", "World"]

    assert rerecipe.extract_by_prefix_surfix(
        text=text,
        prefix="<div>", surfix="</div>",
        include=True,
    ) == ["<div>Hello</div>", "<div>World</div>"]


def test_extract_number():
    for i, j in zip(
        rerecipe.extract_number(
            "Price is $25.99, age is 18, quarter is .25, one is 1."),
        [25.99, 18, 0.25, 1.0],
    ):
        assert abs(i - j) <= 0.0001


def test_extract_email():
    text = '<a href="jobs@gmail.com">My Gmail</a>'
    assert rerecipe.extract_email(text) == ['jobs@gmail.com']


def test_extract_web_url():
    text = '<a href="https://www.google.com">Google</a>'
    assert rerecipe.extract_web_url(text) == ['https://www.google.com']

    text = '<img="https://www.google.com/logo.png">'
    assert rerecipe.extract_web_url(
        text) == ['https://www.google.com/logo.png']


def test_extract_date_iso():
    text = "Release on 2016-01-21"
    assert rerecipe.extract_date_iso(text) == ["2016-01-21"]


def test_extract_date_us():
    text = "Release on 1/21/2016"
    assert rerecipe.extract_date_us(text) == ["1/21/2016"]


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
