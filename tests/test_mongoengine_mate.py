#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mongoengine
from sfm.mongoengine_mate import ExtendedDocument


class User(ExtendedDocument):
    id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()


def test_keys_values_items():
    user = User(id=1, name="Jack")

    assert user.keys() == ["id", "name"]
    assert user.values() == [1, "Jack"]
    assert user.items() == [("id", 1), ("name", "Jack")]


def test_to_tuple_list_dict_OrderedDict_json():
    user = User(id=1, name="Jack")

    assert user.to_tuple() == ("id", "name")
    assert user.to_list() == ["id", "name"]
    assert user.to_dict() == {"id": 1, "name": "Jack"}
    assert user.to_OrderedDict() == {"id": 1, "name": "Jack"}

    assert user.to_json() == '{"_id": 1, "name": "Jack"}'


def test_absorb_and_revise():
    user = User(id=1, name="Jack")
    user.absorb(User(name="Tom"))
    assert user.name == "Tom"

    user_data = {"name": "Mike"}
    user.revise(user_data)
    assert user.name == "Mike"


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
