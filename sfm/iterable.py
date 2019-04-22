# -*- coding: utf-8 -*-

"""
This module provides plenty of useful functions for iterable object manipulation.
"""

import sys
import random
import collections
import itertools
if sys.version_info[0] == 2:
    from itertools import (
        ifilterfalse as filterfalse,
        izip_longest as zip_longest,
        izip as zip,
    )
    string_types = basestring,
else:  # in python3
    from itertools import filterfalse, zip_longest
    string_types = str,


def flatten(iterable):
    """Flatten one layer of nesting.

    Example::

        >>> list(flatten([[0, 1], [2, 3]])
        [0, 1, 2, 3]

        >>> list(flatten(["ab", "cd"])
        ["a", "b", "c", "d"]

    **中文文档**

    将二维列表压平成一维列表。
    """
    return itertools.chain.from_iterable(iterable)


def flatten_all(nested_iterable):
    """Flatten arbitrary depth of nesting. Good for unknown nesting structure
    iterable object.

    Example::

        >>> list(flatten_all([[1, 2], "abc", [3, ["x", "y", "z"]], 4]))
        [1, 2, "abc", 3, "x", "y", "z", 4]

    **中文文档**

    将任意维度的列表压平成一维列表。

    注: 使用hasattr(i, "__iter__")方法做是否是可循环对象的判断, 性能要高于其他
    任何方法, 例如: isinstance(i, collections.Iterable)
    """
    for item in nested_iterable:
        if hasattr(item, "__iter__") and not isinstance(item, string_types):
            for i in flatten_all(item):
                yield i
        else:
            yield item


def nth(iterable, n, default=None):
    """Returns the nth item or a default value.

    Example::

        >>> nth([0, 1, 2], 1)
        1

        >>> nth([0, 1, 2], 100)
        None

    **中文文档**

    取出一个可循环对象中的第n个元素。等效于list(iterable)[n], 但占用极小的内存。
    因为list(iterable)要将所有元素放在内存中并生成一个新列表。该方法常用语对于
    那些取index操作被改写了的可循环对象。
    """
    return next(itertools.islice(iterable, n, None), default)


def take(iterable, n):
    """Return first n items of the iterable as a list.

    Example::

        >>> take([0, 1, 2], 2)
        [0, 1]

    **中文文档**

    取出可循环对象中的前n个元素。等效于list(iterable)[:n], 但占用极小的内存。
    因为list(iterable)要将所有元素放在内存中并生成一个新列表。该方法常用语对于
    那些取index操作被改写了的可循环对象。
    """
    return list(itertools.islice(iterable, n))


def pull(iterable, n):
    """Return last n items of the iterable as a list.

    Example::

        >>> pull([0, 1, 2], 3)
        [1, 2]

    **中文文档**

    取出可循环对象中的最后n个元素。等效于list(iterable)[-n:], 但占用极小的内存。
    因为list(iterable)要将所有元素放在内存中并生成一个新列表。该方法常用语对于
    那些取index操作被改写了的可循环对象。
    """
    fifo = collections.deque(maxlen=n)
    for i in iterable:
        fifo.append(i)
    return list(fifo)


def shuffled(iterable):
    """Returns the shuffled iterable.

    Example::

        >>> shuffled([0, 1, 2])
        [2, 0, 1]

    **中文文档**

    打乱一个可循环对象中所有元素的顺序。并打包成列表返回。
    """
    return random.sample(iterable, len(iterable))


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks.

    Example::

        >>> list(grouper(range(10), n=3, fillvalue=None))
        [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, None, None)]

    **中文文档**

    将一个序列按照尺寸n, 依次打包输出, 如果元素不够n的包, 则用 ``fillvalue`` 中的值填充。
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def grouper_list(l, n):
    """Evenly divide list into fixed-length piece, no filled value if chunk
    size smaller than fixed-length.

    Example::

        >>> list(grouper(range(10), n=3)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    **中文文档**

    将一个列表按照尺寸n, 依次打包输出, 有多少输出多少, 并不强制填充包的大小到n。

    下列实现是按照性能从高到低进行排列的:

    - 方法1: 建立一个counter, 在向chunk中添加元素时, 同时将counter与n比较, 如果一致
      则yield。然后在最后将剩余的item视情况yield。
    - 方法2: 建立一个list, 每次添加一个元素, 并检查size。
    - 方法3: 调用grouper()函数, 然后对里面的None元素进行清理。
    """
    chunk = list()
    counter = 0
    for item in l:
        counter += 1
        chunk.append(item)
        if counter == n:
            yield chunk
            chunk = list()
            counter = 0
    if len(chunk) > 0:
        yield chunk


def grouper_dict(d, n, dict_type=dict):
    """Evenly divide dictionary into fixed-length piece, no filled value if
    chunk size smaller than fixed-length. Notice: dict is unordered in python,
    this method suits better for collections.OrdereDict

    Example::
        >>> d = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        >>> list(grouper_dict(d, 2)
        [{"a": 1, "b": 2}, {"c": 3, "d": 4}, {"e": 5}]

    **中文文档**

    将一个列表按照尺寸n, 依次打包输出, 有多少输出多少, 并不强制填充包的大小到n。
    """
    chunk = dict_type()
    counter = 0
    for k, v in d.items():
        counter += 1
        chunk[k] = v
        if counter == n:
            yield chunk
            chunk = dict_type()
            counter = 0
    if len(chunk) > 0:
        yield chunk

#--- Window ---


def running_window(iterable, size):
    """Generate n-size running window.

    Example::

        >>> for i in running_windows([1, 2, 3, 4, 5], size=3):
        ...     print(i)
        [1, 2, 3]
        [2, 3, 4]
        [3, 4, 5]

    **中文文档**

    简单滑窗函数。
    """
    if size > len(iterable):
        raise ValueError("size can not be greater than length of iterable.")

    fifo = collections.deque(maxlen=size)
    for i in iterable:
        fifo.append(i)
        if len(fifo) == size:
            yield list(fifo)


def cycle_running_window(iterable, size):
    """Generate n-size cycle running window.

    Example::

        >>> for i in running_windows([1, 2, 3, 4, 5], size=3):
        ...     print(i)
        [1, 2, 3]
        [2, 3, 4]
        [3, 4, 5]
        [4, 5, 1]
        [5, 1, 2]

    **中文文档**

    循环位移滑窗函数。
    """
    if size > len(iterable):
        raise ValueError("size can not be greater than length of iterable.")

    fifo = collections.deque(maxlen=size)
    cycle = itertools.cycle(iterable)
    counter = itertools.count(1)
    length = len(iterable)
    for i in cycle:
        fifo.append(i)
        if len(fifo) == size:
            yield list(fifo)
            if next(counter) == length:
                break

#--- Cycle ---


def cycle_slice(sliceable, start, end):
    """Given a list, return right hand cycle direction slice from start to end.

    Example::

        >>> array = [0, 1, 2, 3]
        >>> cycle_slice(array, 1, 3) # from array[1] to array[3]
        [1, 2]

        >>> cycle_slice(array, 3, 1) # from array[3] to array[1]
        [3, 0]

    **中文文档**

    """
    if type(sliceable) != list:
        sliceable = list(sliceable)
    length = len(sliceable)

    if length == 0:
        raise ValueError("sliceable cannot be empty!")
    start = start % length
    end = end % length

    if end > start:
        return sliceable[start:end]
    elif end <= start:
        return sliceable[start:] + sliceable[:end]


def cycle_dist(x, y, perimeter):
    """Find Distance between x, y by means of a n-length cycle.

    :param x:
    :param y:
    :param perimeter:

    Example:

        >>> cycle_dist(1, 23, 24) = 2
        >>> cycle_dist(5, 13, 24) = 8
        >>> cycle_dist(0.0, 2.4, 1.0) = 0.4
        >>> cycle_dist(0.0, 2.6, 1.0) = 0.4

    **中文文档**

    假设坐标轴是一个环, 计算两点之间在环上的最短距离。
    """
    dist = abs(x - y) % perimeter
    if dist > 0.5 * perimeter:
        dist = perimeter - dist
    return dist


#--- Shift ---
def cyclic_shift(array, dist):
    """

    :params array: list like iterable object
    :params dist: int

    Example::

        >>> cyclic_shift([0, 1, 2], 1)
        [2, 0, 1]

        >>> cyclic_shift([0, 1, 2], -1)
        [1, 2, 0]

    **中文文档**

    循环位移函数。
    """
    dist = dist % len(array)
    return array[-dist:] + array[:-dist]


def shift_and_trim(array, dist):
    """Shift and trim unneeded item.

    :params array: list like iterable object
    :params dist: int

    Example::

        >>> array = [0, 1, 2]

        >>> shift_and_trim(array, 0)
        [0, 1, 2]
        >>> shift_and_trim(array, 1)
        [0, 1]

        >>> shift_and_trim(array, -1)
        [1, 2]

        >>> shift_and_trim(array, 3)
        []

        >>> shift_and_trim(array, -3)
        []
    """
    length = len(array)
    if length == 0:
        return []

    if (dist >= length) or (dist <= -length):
        return []
    elif dist < 0:
        return array[-dist:]
    elif dist > 0:
        return array[:-dist]
    else:
        return list(array)


def shift_and_pad(array, dist, pad="__null__"):
    """Shift and pad with item.

    :params array: list like iterable object
    :params dist: int
    :params pad: any value

    Example::

        >>> array = [0, 1, 2]
        >>> shift_and_pad(array, 0)
        [0, 1, 2]

        >>> shift_and_pad(array, 1)
        [0, 0, 1]

        >>> shift_and_pad(array, -1)
        [1, 2, 2]

        >>> shift_and_pad(array, 3)
        [0, 0, 0]

        >>> shift_and_pad(array, -3)
        [2, 2, 2]

        >>> shift_and_pad(array, -1, None)
        [None, 0, 1]
    """
    length = len(array)
    if length == 0:
        return []

    if pad == "__null__":
        if dist > 0:
            padding_item = array[0]
        elif dist < 0:
            padding_item = array[-1]
        else:
            padding_item = None
    else:
        padding_item = pad

    if abs(dist) >= length:
        return length * [padding_item, ]
    elif dist == 0:
        return list(array)
    elif dist > 0:
        return [padding_item, ] * dist + array[:-dist]
    elif dist < 0:
        return array[-dist:] + [padding_item, ] * -dist
    else:  # Never get in this logic
        raise Exception


def size_of_generator(generator, memory_efficient=True):
    """Get number of items in a generator function.

    - memory_efficient = True, 3 times slower, but memory_efficient.
    - memory_efficient = False, faster, but cost more memory.

    **中文文档**

    计算一个生成器函数中的元素的个数。使用memory_efficient=True的方法可以避免将生成器中的
    所有元素放入内存, 但是速度稍慢于memory_efficient=False的方法。
    """
    if memory_efficient:
        counter = 0
        for _ in generator:
            counter += 1
        return counter
    else:
        return len(list(generator))

# Function


def difference(array, k=1):
    """Calculate l[n] - l[n-k]
    """
    if (len(array) - k) < 1:
        raise ValueError()
    if k < 0:
        raise ValueError("k has to be greater or equal than zero!")
    elif k == 0:
        return [i - i for i in array]
    else:
        return [j - i for i, j in zip(array[:-k], array[k:])]
