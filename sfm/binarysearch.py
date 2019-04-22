# -*- coding: utf-8 -*-

"""
This module is provide methods for searching item in a sorted list.

Highlight:

- :func:`find_last_true`: A magic pluggable method, read API reference for more
  info.
- :func:`find_nearest`: Find the nearest item of x from sorted array.

**中文文档**

下面是一些讨论:

原生的 ``bisect.bisect_left`` 和 ``bisect.bisect_right`` 方法返回的是被搜索元素的
index。而Python原生的list的getitem方法的效率并不够快, 所以当我们对一个有序大数组
重复搜索时, 我们最好使用一个: 元素有序, 访问复杂度为O(1)的数据结构。这个数据结构
是什么, 还留给读者思考。
"""

from __future__ import print_function
import bisect

########################################################################
# official recepi from doc.python.org                                  #
# https://docs.python.org/2/library/bisect.html#searching-sorted-lists #
########################################################################


def find_index(array, x):
    """
    Locate the leftmost value exactly equal to x.

    :type array: list
    :param array: an iterable object that support inex

    :param x: a comparable value

    **中文文档**

    返回第一个值等于x的元素的索引。
    """
    i = bisect.bisect_left(array, x)
    if i != len(array) and array[i] == x:
        return i
    raise ValueError


def find_lt(array, x):
    """
    Find rightmost value less than x.

    :type array: list
    :param array: an iterable object that support inex

    :param x: a comparable value

    Example::

        >>> find_lt([0, 1, 2, 3], 2.5)
        2

    **中文文档**

    寻找最大的小于x的数。
    """
    i = bisect.bisect_left(array, x)
    if i:
        return array[i - 1]
    raise ValueError


def find_le(array, x):
    """
    Find rightmost value less than or equal to x.

    :type array: list
    :param array: an iterable object that support inex

    :param x: a comparable value

    Example::

        >>> find_le([0, 1, 2, 3], 2.0)
        2

    **中文文档**

    寻找最大的小于等于x的数。
    """
    i = bisect.bisect_right(array, x)
    if i:
        return array[i - 1]
    raise ValueError


def find_gt(array, x):
    """
    Find leftmost value greater than x.

    :type array: list
    :param array: an iterable object that support inex

    :param x: a comparable value

    Example::

        >>> find_gt([0, 1, 2, 3], 0.5)
        1

    **中文文档**

    寻找最小的大于x的数。
    """
    i = bisect.bisect_right(array, x)
    if i != len(array):
        return array[i]
    raise ValueError


def find_ge(array, x):
    """
    Find leftmost item greater than or equal to x.

    :type array: list
    :param array: an iterable object that support inex

    :param x: a comparable value

    Example::

        >>> find_ge([0, 1, 2, 3], 1.0)
        1

    **中文文档**

    寻找最小的大于等于x的数。
    """
    i = bisect.bisect_left(array, x)
    if i != len(array):
        return array[i]
    raise ValueError


def find_nearest(sorted_list, x):
    """
    Find the nearest item of x from sorted array.

    :type array: list
    :param array: an iterable object that support inex

    :param x: a comparable value

    note: for finding the nearest item from a descending array, I recommend
    find_nearest(sorted_list[::-1], x). Because the built-in list[::-1] method
    is super fast.

    Usage::

        >>> find_nearest([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 5.1)
        5

    **中文文档**

    在正序数组中, 返回最接近x的数。
    """
    if x <= sorted_list[0]:
        return sorted_list[0]
    elif x >= sorted_list[-1]:
        return sorted_list[-1]
    else:
        lower = find_le(sorted_list, x)
        upper = find_ge(sorted_list, x)
        if (x - lower) > (upper - x):
            return upper
        else:
            return lower


def find_last_true(sorted_list, true_criterion):
    """
    Suppose we have a list of item [item1, item2, ..., itemN].

    :type array: list
    :param array: an iterable object that support inex

    :param x: a comparable value

    If we do a mapping::

        >>> def true_criterion(item):
        ...     return item <= 6
        >>> [true_criterion(item) for item in sorted_list]
        [True, True, ... True(last true), False, False, ... False]

    this function returns the index of last true item.

    we do can do the map for all item, and run a binary search to find the 
    index. But sometime the mapping function is expensive. This method avoid
    run mapping function for all items.

    Example::

        array     = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        index     = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        criterion = def true_criterion(x): return x <= 6
        boolean   = [1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

    Solution::

        # first, we check index = int((0 + 9)/2.0) = 4, it's True. 
        # Then check array[4 + 1], it's still True. 
        # Then we jump to int((4 + 9)/2.0) = 6, it's True. 
        # Then check array[6 + 1], ite's False. So array[6] is the one we need.

        >>> find_last_true([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], true_criterion)
        6

    **中文文档**

    功能: 假设有一组排序号了的元素, 从前往后假设前面的元素都满足某一条件, 而到了
    中间某处起就不再满足了。本函数返回满足这一条件的最后一个元素。这在当检验是否
    满足条件本身开销较大时, 能节约大量的计算时间。例如你要判定一系列网页中, 从
    page1 到 page999, 从第几页开始出现404错误。假设是第400个, 那么如果一个个地
    去试, 需要400次, 那如果从0 - 999之间去试, 只需要试验9次即可 (2 ** 9 = 512)

    算法: 

    我们检验最中间的元素, 如果为False, 那么则检验左边所有未检验过的元素的最中间
    的那个。如果为True, 那么检验右边所有未检验过的元素的最中间那个。重复这一过程
    直到被检验的元素为True, 而下一个元素为False, 说明找到了。

    例题::

        有序数组    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        序号        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        条件        小于等于6
        真值表      [1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

    解::

        第一次检查``index = int((0+9)/2.0) = 4``, 为True,
        检查array[4+1], 也是True。那么跳跃至``int((4+9)/2.0)=6``, 为True,。
        再检查array[6+1], 为False, 很显然, 我们找到了。
    """

    # exam first item, if not true, then impossible to find result
    if not true_criterion(sorted_list[0]):
        raise ValueError

    # exam last item, if true, it is the one.
    if true_criterion(sorted_list[-1]):
        return sorted_list[-1]

    lower, upper = 0, len(sorted_list) - 1

    index = int((lower + upper) / 2.0)
    while 1:
        if true_criterion(sorted_list[index]):
            if true_criterion(sorted_list[index + 1]):
                lower = index
                index = int((index + upper) / 2.0)
            else:
                return index
        else:
            upper = index
            index = int((lower + index) / 2.0)
