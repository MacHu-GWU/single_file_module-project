#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module extend the power of mongoengine.
"""

from collections import OrderedDict


class ExtendedDocument(object):

    """Provide `mongoengine.Document <http://docs.mongoengine.org/apireference.html#mongoengine.Document>`_
    more utility methods.

    **中文文档**

    为默认的 ``mongoengine.Document`` 提供了更多的便捷方法。
    """

    def keys(self):
        try:
            return list(self._fields_ordered)
        except AttributeError:
            raise TypeError("It does not inherit from mongoengine.Document!")

    def values(self):
        return [self._data.get(attr) for attr in self.keys()]

    def items(self):
        return [(attr, self._data.get(attr)) for attr in self.keys()]

    def to_tuple(self):
        return self._fields_ordered

    def to_list(self):
        return self.keys()

    def to_dict(self):
        return dict(self.items())

    def to_OrderedDict(self):
        return OrderedDict(self.items())


#--- Unittest ---
def test_ExtendedDocument():
    import mongoengine

    class User(mongoengine.Document, ExtendedDocument):
        id = mongoengine.IntField(primary_key=True)
        name = mongoengine.StringField()

        meta = {"collection": "user"}

    user = User(id=1, name="Jack")
    assert user.keys() == ["id", "name"]
    assert user.values() == [1, "Jack"]
    assert user.items() == [("id", 1), ("name", "Jack")]

    od = user.to_OrderedDict()
    assert od["id"] == 1
    assert od["name"] == "Jack"

    class Item(ExtendedDocument):

        def __init__(self, id, name):
            self.id = id
            self.name = name

    item = Item(id=1, name="egg")
    try:
        item.to_dict()  # a type error will be raise
    except TypeError:
        pass


if __name__ == "__main__":
    test_ExtendedDocument()
