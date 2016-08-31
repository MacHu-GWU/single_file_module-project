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
    

def test_absorb():
    user1 = User(id=1, name="Jack")
    user2 = User(name="Tom")
    user1.absorb(user2)
    assert user1.id == 1
    assert user1.name == "Tom"
    
    
if __name__ == "__main__":
    import py
    import os
    py.test.cmdline.main("%s --tb=native -s" % os.path.basename(__file__))