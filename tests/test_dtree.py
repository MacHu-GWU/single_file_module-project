#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
import string
from pprint import pprint as ppt
from sfm.dtree import DictTree


dt = DictTree(name="United State")
dt["MD"] = DictTree(name="Maryland")
dt["VA"] = DictTree(name="Virginia")

dt["MD"]["Gaithersburg"] = DictTree(zipcode="20878")
dt["MD"]["College Park"] = DictTree(zipcode="20740")

dt["VA"]["Arlington"] = DictTree(zipcode="22202")
dt["VA"]["Fairfax"] = DictTree(zipcode="20030")


def test_setattr_getattr():
    dt = DictTree()
    dt.name = "USA"
    assert dt.name == "USA"


def test_setitem_getitem():
    dt = DictTree()
    dt.name = "USA"

    dt_MD = DictTree(name="Maryland")
    dt["MD"] = dt_MD
    assert dt["MD"].name == "Maryland"
    assert dt["MD"].__data__ == dt_MD.__data__


def test_iter():
    keys = list(dt.keys())
    keys.sort()
    assert keys == ["MD", "VA"]

    for value in dt.values():
        assert isinstance(value, DictTree)


def test_keys_at():
    keys = list(dt.keys_at(0))
    keys.sort()
    assert keys == ["__root__"]

    keys = list(dt.keys_at(1))
    keys.sort()
    assert keys == ["MD", "VA"]

    keys = list(dt.keys_at(2))
    keys.sort()
    assert keys == ["Arlington", "College Park", "Fairfax", "Gaithersburg"]


def test_values_at():
    names = [value.__data__["__meta__"]["name"] for value in dt.values_at(0)]
    names.sort()
    names == ["United State"]

    names = [value.__data__["__meta__"]["name"] for value in dt.values_at(1)]
    names.sort()
    names == ["Maryland", "Virginia"]

    zipcodes = [value.__data__["__meta__"]["zipcode"]
                for value in dt.values_at(2)]
    zipcodes.sort()
    zipcodes == ["20030", "20740", "20878", "22202"]


def test_items_at():
    keys = [key for key, value in dt.items_at(0)]
    keys.sort()
    assert keys == ["__root__"]

    keys = [key for key, value in dt.items_at(1)]
    keys.sort()
    assert keys == ["MD", "VA"]

    keys = [key for key, value in dt.items_at(2)]
    keys.sort()
    assert keys == ["Arlington", "College Park", "Fairfax", "Gaithersburg"]


def test_length_at():
    assert dt.length_at(0) == 1
    assert dt.length_at(1) == 2
    assert dt.length_at(2) == 4


def test_mutable():
    """

    **中文文档**

    测试对子树的修改, 是不是也会修改母树。(应该是会)
    """
    usa = DictTree(name="USA", pop=200 * 10 ** 6)  # 创建母树
    usa["VA"] = DictTree(name="VA", pop=3 * 10 ** 6)  # 创建子树
    dt = usa["VA"]  # 获取子树
    dt.pop = 999999  # 修改子树的属性

    # 看是否也修改了母树的__data__
    assert usa.__data__["VA"]["__meta__"]["pop"] == 999999


def test_stats_at():
    result = dt.stats()

    assert result[0]["depth"] == 0
    assert result[0]["leaf"] == 0
    assert result[0]["root"] == 1

    assert result[1]["depth"] == 1
    assert result[1]["leaf"] == 0
    assert result[1]["root"] == 2

    assert result[2]["depth"] == 2
    assert result[2]["leaf"] == 4
    assert result[2]["root"] == 0


def rand_str(length):
    return "".join([random.choice(options) for _ in range(length)])


if __name__ == "__main__":
    import py
    import os
    py.test.cmdline.main("%s --tb=native -s" % os.path.basename(__file__))
