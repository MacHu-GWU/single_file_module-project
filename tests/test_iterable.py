#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import time
from collections import OrderedDict
from sfm import iterable


def test_flatten():
    """测试 :func:`~sfm.iterable.flatten`  的功能。
    """
    assert list(iterable.flatten([[1, 2], [3, 4]])) == [1, 2, 3, 4]
    assert list(iterable.flatten([["a", "b"], ["c", "d"]])) == [
        "a", "b", "c", "d"]
    assert list(iterable.flatten(["ab", "cd"])) == ["a", "b", "c", "d"]


def test_flatten_performance():
    """测试 :func:`~sfm.iterable.flatten`  的性能。

    **中文文档**

    测试是否用itertools实现的flatten性能要优于直接使用for循环实现。
    """
    def another_flatten(nested_iterable):
        """An intuitive implementation.
        """
        for iterable in nested_iterable:
            for i in iterable:
                yield i

    list_of_list = [list(range(1000)) for _ in range(1000)]

    st = time.clock()
    list(iterable.flatten(list_of_list))
    elapsed1 = time.clock() - st

    st = time.clock()
    list(another_flatten(list_of_list))
    elapsed2 = time.clock() - st

    assert elapsed1 < elapsed2


def test_flatten_all():
    """测试 :func:`~sfm.iterable.flatten_all`  的功能。
    """
    nested_iterable = [[1, 2], "abc", [3, ["x", "y", "z"]], 4]
    assert list(iterable.flatten_all(nested_iterable)) == [
        1, 2, "abc", 3, "x", "y", "z", 4]


def test_nth():
    """测试 :func:`~sfm.iterable.nth`  的功能。
    """
    array = [0, 1, 2]
    assert iterable.nth(array, 1) == 1
    assert iterable.nth(array, 3) == None


def test_take():
    """测试 :func:`~sfm.iterable.take`  的功能。
    """
    array = [0, 1, 2]
    assert iterable.take(array, 0) == []
    assert iterable.take(array, 1) == [0]
    assert iterable.take(array, 2) == [0, 1]
    assert iterable.take(array, 3) == [0, 1, 2]


def test_pull():
    """测试 :func:`~sfm.iterable.pull`  的功能。
    """
    array = [0, 1, 2]
    assert iterable.pull(array, 0) == []
    assert iterable.pull(array, 1) == [2, ]
    assert iterable.pull(array, 2) == [1, 2]
    assert iterable.pull(array, 3) == [0, 1, 2]


def test_shuffled():
    """测试 :func:`~sfm.iterable.shuffled`  的功能。
    """
    array = list(range(1000))
    assert iterable.shuffled(range(1000)) != array


def test_grouper():
    """测试 :func:`~sfm.iterable.grouper`  的功能。
    """
    l = [1, 2, 3]
    assert list(iterable.grouper(l, 2)) == [(1, 2), (3, None)]


def test_grouper_list():
    """测试 :func:`~sfm.iterable.grouper_list`  的功能。
    """
    l = [1, 2, 3, 4]
    assert list(iterable.grouper_list(l, 2)) == [[1, 2], [3, 4]]

    l = [1, 2, 3, 4, 5]
    assert list(iterable.grouper_list(l, 2)) == [[1, 2], [3, 4], [5, ], ]


def test_grouper_dict():
    """测试 :func:`~sfm.iterable.grouper_dict`  的功能。
    """
    d = OrderedDict([("a", 1), ("b", 2), ("c", 3), ("d", 4)])
    assert list(iterable.grouper_dict(d, 2)) == [
        {"a": 1, "b": 2}, {"c": 3, "d": 4}]

    d = OrderedDict([("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)])
    assert list(iterable.grouper_dict(d, 2)) == [
        {"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5}, ]


def test_size_of_generator():
    """测试 :func:`~sfm.iterable.size_of_generator`  的性能。
    """
    def number_generator():
        for i in range(1000 * 1000):
            yield i

    st = time.clock()
    n1 = iterable.size_of_generator(number_generator(), memory_efficient=True)
    elapse1 = time.clock() - st

    st = time.clock()
    n2 = iterable.size_of_generator(number_generator(), memory_efficient=False)
    elapse2 = time.clock() - st

    assert n1 == n2 == 1000 * 1000


def test_running_window():
    """测试 :func:`~sfm.iterable.running_window`  的功能。
    """
    assert list(iterable.running_window([1, 2, 3, 4, 5], 3)) == [
        [1, 2, 3], [2, 3, 4], [3, 4, 5],
    ]
    assert list(iterable.running_window([1, 2, 3], 3)) == [[1, 2, 3], ]
    with pytest.raises(ValueError):
        list(iterable.running_window([1, 2, 3], 4))


def test_cycle_running_window():
    """测试 :func:`~sfm.iterable.cycle_running_window` 的功能。
    """
    assert list(iterable.cycle_running_window([1, 2, 3, 4, 5], 3)) == [
        [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 1], [5, 1, 2],
    ]
    assert list(iterable.cycle_running_window([1, 2, 3], 3)) == [
        [1, 2, 3], [2, 3, 1], [3, 1, 2],
    ]
    with pytest.raises(ValueError):
        list(iterable.cycle_running_window([1, 2, 3], 4))


def test_cycle_slice():
    """测试 :func:`~sfm.iterable.cycle_slice`  的功能。
    """
    array = [0, 1, 2, 3]
    assert iterable.cycle_slice(array, 1, 3) == [1, 2]
    assert iterable.cycle_slice(array, 3, 1) == [3, 0]
    assert iterable.cycle_slice(array, 0, 0) == [0, 1, 2, 3]
    assert iterable.cycle_slice(array, 2, 2) == [2, 3, 0, 1]

    assert iterable.cycle_slice(array, 5, -1) == [1, 2]

    array = [0, ]
    assert iterable.cycle_slice(array, 1, 2) == [0, ]

    with pytest.raises(ValueError):
        iterable.cycle_slice([], 1, 2)


def test_cycle_dist():
    """测试 :func:`~sfm.iterable.cycle_dist`  的功能。
    """
    assert iterable.cycle_dist(1, 23, 24) == 2
    assert iterable.cycle_dist(5, 13, 24) == 8
    assert iterable.cycle_dist(0, 4, 10) == 4
    assert iterable.cycle_dist(0, 6, 10) == 4


def test_cyclic_shift():
    """测试 :func:`~sfm.iterable.cyclic_shift`  的功能。
    """
    array = [0, 1, 2]
    assert iterable.cyclic_shift(array, 0) == [0, 1, 2]
    assert iterable.cyclic_shift(array, 1) == [2, 0, 1]
    assert iterable.cyclic_shift(array, 2) == [1, 2, 0]
    assert iterable.cyclic_shift(array, -1) == [1, 2, 0]
    assert iterable.cyclic_shift(array, -2) == [2, 0, 1]


def test_shift_and_trim():
    """测试 :func:`~sfm.iterable.shift_and_trim`  的功能。
    """
    array = [0, 1, 2]
    assert iterable.shift_and_trim(array, 0) == [0, 1, 2]
    assert iterable.shift_and_trim(array, 1) == [0, 1]
    assert iterable.shift_and_trim(array, -1) == [1, 2]
    assert iterable.shift_and_trim(array, 3) == []
    assert iterable.shift_and_trim(array, -3) == []


def test_shift_and_pad():
    """测试 :func:`~sfm.iterable.shift_and_pad`  的功能。
    """
    array = [0, 1, 2]
    assert iterable.shift_and_pad(array, 0) == [0, 1, 2]
    assert iterable.shift_and_pad(array, 1) == [0, 0, 1]
    assert iterable.shift_and_pad(array, 2) == [0, 0, 0]
    assert iterable.shift_and_pad(array, 3) == [0, 0, 0]
    assert iterable.shift_and_pad(array, 3, None) == [None, None, None]

    assert iterable.shift_and_pad(array, -1) == [1, 2, 2]
    assert iterable.shift_and_pad(array, -2) == [2, 2, 2]
    assert iterable.shift_and_pad(array, -3) == [2, 2, 2]
    assert iterable.shift_and_pad(array, -3, None) == [None, None, None]


def test_difference():
    assert iterable.difference([1, 2, 3], 0) == [0, 0, 0]
    assert iterable.difference([1, 2, 3], 1) == [1, 1]
    assert iterable.difference([1, 2, 3], 2) == [2,]
    
    with pytest.raises(ValueError):
        iterable.difference([1, 2, 3], -1)
    
    with pytest.raises(ValueError):
        iterable.difference([1, 2, 3], 3)
            
            
if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
