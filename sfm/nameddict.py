#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Similar to ``collections.namedtuple``, ``nameddict`` is a data container class.

**中文文档**

和 ``collections.namedtuple`` 类似, ``nameddict`` 是一种数据容器类。提供了方便的方法
对属性, 值进行for循环, 以及和list, dict之间的IO交互。
"""

import json
from collections import OrderedDict


class Base(object):
    """nameddict base class.
    """
    __attrs__ = None

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            object.__setattr__(self, attr, value)

    def __repr__(self):
        kwargs = list()
        for attr, value in self.items():
            kwargs.append("%s=%r" % (attr, value))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(kwargs))

    @classmethod
    def _make(cls, d):
        return cls(**d)

    def keys(self):
        return [key for key, value in self.items()]

    def values(self):
        return [value for key, value in self.items()]

    def items(self):
        if self.__attrs__ is None:
            return list(sorted(self.__dict__.items(), key=lambda x: x[0]))
        try:
            return [(attr, self.__dict__.get(attr)) for attr in self.__attrs__]
        except:
            raise AttributeError()

    def __iter__(self):
        if self.__attrs__ is None:
            return iter(self.keys())
        try:
            return iter(self.__attrs__)
        except:
            raise AttributeError()

    def to_list(self):
        return self.keys()

    def to_dict(self):
        return dict(self.items())

    def to_OrderedDict(self):
        return OrderedDict(self.items())

    def to_json(self):
        return json.dumps(self.to_dict())

#--- Unittest ---


def test_Base():
    # Style 1
    class Person(Base):
        def __init__(self, id, name, email):
            self.id = id
            self.name = name
            self.email = email

    person = Person(id=1, name="Jack", email="jack@example.com")
    assert str(person) == "Person(email='jack@example.com', id=1, name='Jack')"
    assert person.items() == [
        ("email", "jack@example.com"), ("id", 1), ("name", "Jack")]
    assert list(person) == ["email", "id", "name"]

    person = Person._make(
        {"id": 1, "name": "Jack", "email": "jack@example.com"})
    assert str(person) == "Person(email='jack@example.com', id=1, name='Jack')"
    assert person.items() == [
        ("email", "jack@example.com"), ("id", 1), ("name", "Jack")]
    assert list(person) == ["email", "id", "name"]

    # Style 2
    class Person(Base):
        __attrs__ = ["id", "name"]

    person = Person(id=1, name="Jack", email="jack@example.com")
    assert str(person) == "Person(id=1, name='Jack')"
    assert person.items() == [("id", 1), ("name", "Jack")]
    assert list(person) == ["id", "name"]

    person = Person._make(
        {"id": 1, "name": "Jack", "email": "jack@example.com"})
    assert str(person) == "Person(id=1, name='Jack')"
    assert person.items() == [("id", 1), ("name", "Jack")]
    assert list(person) == ["id", "name"]

if __name__ == "__main__":
    test_Base()
