# -*- coding: utf-8 -*-

"""
Similar to ``collections.namedtuple``, ``nameddict`` is a data container class.
Provides methods to iterate on attributes and values.

**中文文档**

和 ``collections.namedtuple`` 类似, ``nameddict`` 是一种数据容器类。提供了方便的方法
对属性, 值进行for循环, 以及和list, dict之间的IO交互。
"""

import json
import copy
from collections import OrderedDict
from functools import total_ordering


@total_ordering
class Base(object):

    """nameddict base class.
    """
    __attrs__ = None
    """该属性非常重要, 定义了哪些属性被真正视为 ``attributes``, 换言之, 就是在
    :meth:`~Base.keys()`, :meth:`~Base.values()`, :meth:`~Base.items()`,
    :meth:`~Base.to_list()`, :meth:`~Base.to_dict()`, :meth:`~Base.to_OrderedDict()`,
    :meth:`~Base.to_json()`, 方法中要被包括的属性。
    """

    __excludes__ = []
    """在此被定义的属性将不会出现在 :meth:`~Base.items()` 中
    """

    __reserved__ = set(["keys", "values", "items"])

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __setattr__(self, attr, value):
        if attr in self.__reserved__:
            raise ValueError("%r is a reserved attribute name!" % attr)
        object.__setattr__(self, attr, value)

    def __repr__(self):
        kwargs = list()
        for attr, value in self.items():
            kwargs.append("%s=%r" % (attr, value))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(kwargs))

    def __getitem__(self, key):
        """Access attribute.
        """
        return object.__getattribute__(self, key)

    @classmethod
    def _make(cls, d):
        """Make an instance.
        """
        return cls(**d)

    def items(self):
        """items按照属性的既定顺序返回attr, value对。当 ``__attrs__`` 未指明时,
        则按照字母顺序返回。若 ``__attrs__`` 已定义时, 按照其中的顺序返回。

        当有 ``@property`` 装饰器所装饰的属性时, 若没有在 ``__attrs__`` 中定义,
        则items中不会包含它。
        """
        items = list()

        if self.__attrs__ is None:
            for key, value in self.__dict__.items():
                if key not in self.__excludes__:
                    items.append((key, value))
            items = list(sorted(items, key=lambda x: x[0]))
            return items
        try:
            for attr in self.__attrs__:
                if attr not in self.__excludes__:
                    try:
                        items.append(
                            (attr, copy.deepcopy(getattr(self, attr))))
                    except AttributeError:
                        items.append(
                            (attr, copy.deepcopy(self.__dict__.get(attr))))
            return items
        except:
            raise AttributeError()

    def keys(self):
        """Iterate attributes name.
        """
        return [key for key, value in self.items()]

    def values(self):
        """Iterate attributes value.
        """
        return [value for key, value in self.items()]

    def __iter__(self):
        """Iterate attributes.
        """
        if self.__attrs__ is None:
            return iter(self.keys())
        try:
            return iter(self.__attrs__)
        except:
            raise AttributeError()

    def to_list(self):
        """Export data to list. Will create a new copy for mutable attribute.
        """
        return self.keys()

    def to_dict(self):
        """Export data to dict. Will create a new copy for mutable attribute.
        """
        return dict(self.items())

    def to_OrderedDict(self):
        """Export data to OrderedDict. Will create a new copy for mutable 
        attribute.
        """
        return OrderedDict(self.items())

    def to_json(self, sort_keys=False, indent=None):
        """Export data to json. If it is json serilizable.
        """
        return json.dumps(self.to_dict(), sort_keys=sort_keys, indent=indent)

    def __eq__(self, other):
        """Equal to.
        """
        return self.items() == other.items()

    def __lt__(self, other):
        """Less than.
        """
        for (_, value1), (_, value2) in zip(self.items(), other.items()):
            if value1 >= value2:
                return False
        return True
