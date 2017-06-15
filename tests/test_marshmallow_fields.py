#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm import marshmallow_fields
from sfm import nameddict
from marshmallow import Schema, fields


class User(nameddict.Base):
    pass


def test_NonEmptyStringField():
    class UserSchema(Schema):
        name = marshmallow_fields.NonEmptyStringField()

    user_schema = UserSchema()

    # load
    assert user_schema.load({"name": None}).data["name"] is None
    assert user_schema.load({"name": ""}).data["name"] is None
    assert user_schema.load({"name": "    "}).data["name"] is None
    assert user_schema.load({"name": "  John  "}).data["name"] == "John"

    # dump
    assert user_schema.dump(User(name=None)).data["name"] is None
    assert user_schema.dump(User(name="")).data["name"] is None
    assert user_schema.dump(User(name="    ")).data["name"] is None
    assert user_schema.dump(User(name="  John  ")).data["name"] == "John"


def test_TitleStringField():
    class UserSchema(Schema):
        name = marshmallow_fields.TitleStringField()

    user_schema = UserSchema()

    # load
    assert user_schema.load({"name": None}).data["name"] is None
    assert user_schema.load({"name": ""}).data["name"] is None
    assert user_schema.load({"name": "    "}).data["name"] is None
    assert user_schema.load(
        {"name": "  john    david  "}).data["name"] == "John David"

    # dump
    assert user_schema.dump(User(name=None)).data["name"] is None
    assert user_schema.dump(User(name="")).data["name"] is None
    assert user_schema.dump(User(name="    ")).data["name"] is None
    assert user_schema.dump(
        User(name="  john    david  ")).data["name"] == "John David"


def test_LowerStringField():
    class UserSchema(Schema):
        name = marshmallow_fields.LowerStringField()

    user_schema = UserSchema()

    # load
    assert user_schema.load({"name": None}).data["name"] is None
    assert user_schema.load({"name": ""}).data["name"] is None
    assert user_schema.load({"name": "    "}).data["name"] is None
    assert user_schema.load({"name": "  John  "}).data["name"] == "john"

    # dump
    assert user_schema.dump({"name": None}).data["name"] is None
    assert user_schema.dump({"name": ""}).data["name"] is None
    assert user_schema.dump({"name": "    "}).data["name"] is None
    assert user_schema.dump({"name": "  John  "}).data["name"] == "john"


def test_UpperStringField():
    class UserSchema(Schema):
        name = marshmallow_fields.UpperStringField()

    user_schema = UserSchema()

    # load
    assert user_schema.load({"name": None}).data["name"] is None
    assert user_schema.load({"name": ""}).data["name"] is None
    assert user_schema.load({"name": "    "}).data["name"] is None
    assert user_schema.load({"name": "  John  "}).data["name"] == "JOHN"

    # dump
    assert user_schema.dump({"name": None}).data["name"] is None
    assert user_schema.dump({"name": ""}).data["name"] is None
    assert user_schema.dump({"name": "    "}).data["name"] is None
    assert user_schema.dump({"name": "  John  "}).data["name"] == "JOHN"


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
