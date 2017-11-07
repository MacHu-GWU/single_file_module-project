#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm import textformatter


def test_format_single_space_only():
    text = " I   feel    so  GOOD!"
    expect = "I feel so GOOD!"
    assert textformatter.format_single_space_only(text) == expect
    assert textformatter.format_single_space_only("") == ""


def test_format_title():
    text = " beautiful  IS   better    Than ugly   "
    expect = "Beautiful is Better than Ugly"
    assert textformatter.format_title(text) == expect
    assert textformatter.format_title("") == ""


def test_format_person_name():
    text = " michael  jackson "
    expect = "Michael Jackson"
    assert textformatter.format_person_name(text) == expect
    assert textformatter.format_person_name("") == ""


def test_format_format_CapitalizedWord():
    text = "  variable  name - is_very__very_good "
    expect = "VariableNameIsVeryVeryGood"
    assert textformatter.format_CapitalizedWord(text) == expect
    assert textformatter.format_person_name("") == ""


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
