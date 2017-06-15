#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from sfm.nameddict import Base


def test_Base():
    # Style 1, __attrs__ is not defined
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

    # Style 2, __attrs__ is defined
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
    """在__attrs__中定义了的@property属性, 是否也能被包含到items()中。
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


def test_excludes_attribute_name():
    class User(Base):
        __attrs__ = ["id", "name", "gender"]
        __excludes__ = ["name"]

    user = User(id=1, name="Jack", gender="male")
    assert user.keys() == ["id", "gender"]


def test_reserved_attribute_name():
    class User(Base):
        pass

    with raises(ValueError):
        user = User(keys=1, values=2)

    class User(Base):

        def __init__(self, keys, values):
            self.keys = keys
            self.values = values

    with raises(Exception):
        user = User(keys="keys", values=1)


def test_comparison():
    class User(Base):
        pass

    user1 = User(id=1)
    user2 = User(id=2)
    assert user1 == user1
    assert user1 < user2
    assert user2 > user1


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
