#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Similar to ``collections.namedtuple``, ``nameddict`` is a data container class.

**中文文档**

和 ``collections.namedtuple`` 类似, ``nameddict`` 是一种数据容器类。提供了方便的方法
对属性, 值进行for循环, 以及和list, dict之间的IO交互。
"""

import json
import copy
from collections import OrderedDict


class Base(object):
    """nameddict base class.
    """
    __attrs__ = None
    """该属性非常重要, 定义了哪些属性被真正视为 ``attributes``, 换言之, 就是在
    :meth:`~Base.keys()`, :meth:`~Base.values()`, :meth:`~Base.items()`,
    :meth:`~Base.to_list()`, :meth:`~Base.to_dict()`, :meth:`~Base.to_OrderedDict()`,
    :meth:`~Base.to_json()`, 方法中要被包括的属性。
    """
    __reserved__ = set(["keys", "values", "items"])
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
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
        return cls(**d)

    def items(self):
        """items按照属性的既定顺序返回attr, value对。当 ``__attrs__`` 未指明时,
        则按照字母顺序返回。若 ``__attrs__`` 已定义时, 按照其中的顺序返回。
        
        当有 ``@property`` 装饰器所装饰的属性时, 若没有在 ``__attrs__`` 中定义,
        则items中不会包含它。
        """
        if self.__attrs__ is None:
            return list(sorted(self.__dict__.items(), key=lambda x: x[0]))
        try:
            items = list()
            for attr in self.__attrs__:
                try:
                    items.append((attr, copy.deepcopy(getattr(self, attr))))
                except AttributeError:
                    items.append((attr, copy.deepcopy(self.__dict__.get(attr))))
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

    def to_json(self):
        """Export data to json. If it is json serilizable.
        """
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


def test_property_decorator():
    """测试在
    """
    class Employee(Base):
        __attrs__ = ["base_salary", "bonus", "total_salary"]
        
        def __init__(self, base_salary, bonus):
            self.base_salary = base_salary
            self.bonus = bonus

    employee = Employee(base_salary=1000, bonus=300)
    assert employee.to_dict()["total_salary"] is None

    class Employee(Base):
        __attrs__ = ["base_salary", "bonus", "total_salary"]
        
        def __init__(self, base_salary, bonus):
            self.base_salary = base_salary
            self.bonus = bonus
        
        @property
        def total_salary(self):
            return self.base_salary + self.bonus

    employee = Employee(base_salary=1000, bonus=300)
    assert employee.to_dict()["total_salary"] == 1300


if __name__ == "__main__":
    test_Base()
    test_property_decorator()