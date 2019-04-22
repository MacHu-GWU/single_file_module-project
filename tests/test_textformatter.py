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


def test_format_camel_case():
    text = "  variable  name - is_very__very_good "
    expect = "VariableNameIsVeryVeryGood"
    assert textformatter.format_camel_case(text) == expect


def test_format_small_camel_case():
    text = "  variable  name - is_very__very_good "
    expect = "variableNameIsVeryVeryGood"
    assert textformatter.format_small_camel_case(text) == expect


def test_format_unix_var():
    text = "  Variable  Name - is_very__very_Good "
    expect = "variable_name_is_very_very_good"
    assert textformatter.format_unix_var(text) == expect


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
