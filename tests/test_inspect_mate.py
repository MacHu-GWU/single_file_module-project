#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm.inspect_mate import *


class Base(object):
    attribute = "attribute"

    @property
    def property_method(self):
        return "property_method"

    def regular_method(self):
        return "regular_method"

    @staticmethod
    def static_method():
        return "static_method"

    @classmethod
    def class_method(cls):
        return "class_method"


class MyClass(Base):
    pass


def export_true_table():
    """Export value, checker function output true table.
    Help to organize thought.
    """
    import pandas as pd

    attr_value_paris = [
        ("attribute", MyClass.attribute),
        ("property_method", MyClass.property_method),
        ("regular_method", MyClass.regular_method),
        ("__dict__['static_method']", Base.__dict__["static_method"]),
        ("__dict__['class_method']", Base.__dict__["class_method"]),
        ("static_method", MyClass.static_method),
        ("class_method", MyClass.class_method),
    ]
    tester_list = [
        ("inspect.isroutine", lambda v: inspect.isroutine(v)),
        ("inspect.isfunction", lambda v: inspect.isfunction(v)),
        ("inspect.ismethod", lambda v: inspect.ismethod(v)),
        ("isinstance.property", lambda v: isinstance(v, property)),
        ("isinstance.staticmethod", lambda v: isinstance(v, staticmethod)),
        ("isinstance.classmethod", lambda v: isinstance(v, classmethod)),
    ]

    df = pd.DataFrame()
    for attr, value in attr_value_paris:
        col = list()
        for name, tester in tester_list:
            if tester(value):
                flag = 1
            else:
                flag = 0
            col.append(flag)
        df[attr] = col
    df.index = [name for name, _ in tester_list]

    import sys

    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3

    if PY2:
        fname = "PY2"
    elif PY3:
        fname = "PY3"

    writer = pd.ExcelWriter("%s.xlsx" % fname)
    df.to_excel(writer, fname, index=True)
    writer.save()

# export_true_table()


def test_is_attribute_property_method_regular_method_static_method_class_method():
    assert is_attribute(MyClass, "attribute", MyClass.attribute)
    assert is_property_method(
        MyClass, "property_method", MyClass.property_method)
    assert is_regular_method(
        MyClass, "regular_method", MyClass.regular_method)
    assert is_static_method(
        MyClass, "static_method", MyClass.static_method)
    assert is_class_method(MyClass, "class_method", MyClass.class_method)

    attr_list = [
        (MyClass, "attribute", MyClass.attribute),
        (MyClass, "property_method", MyClass.property_method),
        (MyClass, "regular_method", MyClass.regular_method),
        (MyClass, "static_method", MyClass.static_method),
        (MyClass, "class_method", MyClass.class_method),
    ]

    checker_list = [
        is_attribute,
        is_property_method,
        is_regular_method,
        is_static_method,
        is_class_method,
    ]

    for i, pair in enumerate(attr_list):
        klass, attr, value = pair
        for j, checker in enumerate(checker_list):
            if i == j:
                assert checker(klass, attr, value) is True
            else:
                assert checker(klass, attr, value) is False


def test_getter():
    def items_to_keys(items):
        return set([item[0] for item in items])

    assert items_to_keys(get_attributes(MyClass)) == {"attribute"}
    assert items_to_keys(
        get_property_methods(MyClass)) == {"property_method"}
    assert items_to_keys(
        get_regular_methods(MyClass)) == {"regular_method"}
    assert items_to_keys(
        get_static_methods(MyClass)) == {"static_method"}
    assert items_to_keys(
        get_class_methods(MyClass)) == {"class_method"}

    assert items_to_keys(
        get_all_attributes(MyClass)) == {"attribute", "property_method"}
    assert items_to_keys(
        get_all_methods(MyClass)) == {"regular_method", "static_method", "class_method"}


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
