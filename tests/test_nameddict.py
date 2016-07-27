#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sfm.nameddict import Base


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
    import py
    import os
    py.test.cmdline.main("%s --tb=native -s" % os.path.basename(__file__))
