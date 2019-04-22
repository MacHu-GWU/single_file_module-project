# -*- coding: utf-8 -*-

import pytest
from sfm.dtree import DictTree, DATA, META, KEY, ROOT


class TestDictTree(object):
    dt_USA = DictTree(name="USA")
    dt_USA["MD"] = DictTree(name="Maryland")
    dt_VA = DictTree(name="Virginia")
    dt_USA["VA"] = dt_VA

    dt_USA["MD"]["Gaithersburg"] = DictTree(name="Gaithersburg", zipcode="20878")
    dt_COLLEGE_PARK = DictTree(name="College Park", zipcode="20740")
    dt_USA["MD"]["College Park"] = dt_COLLEGE_PARK

    dt_USA["VA"]["Arlington"] = DictTree(name="Arlington", zipcode="22202")
    dt_FAIRFAX = DictTree(name="Fairfax", zipcode="20030")
    dt_USA["VA"]["Fairfax"] = dt_FAIRFAX

    def test_key(self):
        dt = DictTree(name="USA")
        assert dt._key() == "__root__"

        dt1 = DictTree(name="Maryland")
        assert dt1._key() == "__root__"

        dt["MD"] = dt1
        assert dt._key() == "__root__"
        assert dt1._key() == "MD"
        assert dt["MD"]._key() == "MD"

    def test_setattr_getattr(self):
        dt_USA = DictTree(name="USA")  # assign metadata when init
        assert dt_USA.name == "USA"

        dt_USA2 = DictTree()  # assign metadata afterward
        dt_USA2.name = "USA"
        assert dt_USA2.name == "USA"

        dt_USA["MD"] = DictTree(name="Maryland")
        assert dt_USA["MD"].name == "Maryland"

        dt_VA = DictTree()
        dt_USA["VA"] = dt_VA
        dt_USA["VA"].name = "Virginia"
        assert dt_USA["VA"].name == "Virginia"

        # test with the universal case
        assert self.dt_USA["MD"].name == "Maryland"
        assert self.dt_USA["VA"].name == "Virginia"
        assert self.dt_USA["MD"]["College Park"].zipcode == "20740"
        assert self.dt_USA["VA"]["Arlington"].zipcode == "22202"

    def test_setitem_getitem(self):
        dt = DictTree()
        dt.name = "USA"

        dt_MD = DictTree(name="Maryland")
        dt["MD"] = dt_MD
        assert dt["MD"].name == "Maryland"
        assert dt["MD"].__data__ == dt_MD.__data__
        assert dt["MD"]._key() == "MD"
        assert dt_MD._key() == "MD"

    def test_iter(self):
        keys = list(self.dt_USA.keys())
        keys.sort()
        assert keys == ["MD", "VA"]

        keys = list(self.dt_USA["VA"])
        keys.sort()
        assert keys == ["Arlington", "Fairfax"]

        keys = list(self.dt_USA["VA"].keys())
        keys.sort()
        assert keys == ["Arlington", "Fairfax"]

        keys = list(self.dt_VA)
        keys.sort()
        assert keys == ["Arlington", "Fairfax"]

        keys = list(self.dt_VA.keys())
        keys.sort()
        assert keys == ["Arlington", "Fairfax"]

        for value in self.dt_USA.values():
            assert isinstance(value, DictTree)

        for key, value in self.dt_USA.items():
            assert key in ["MD", "VA"]
            assert isinstance(value, DictTree)

    def test_keys_at(self):
        keys = list(self.dt_USA.keys_at(0))
        keys.sort()
        assert keys == [ROOT, ]

        keys = list(self.dt_USA.keys_at(1))
        keys.sort()
        assert keys == ["MD", "VA"]

        keys = list(self.dt_USA.keys_at(2))
        keys.sort()
        assert keys == ["Arlington", "College Park", "Fairfax", "Gaithersburg"]

    def test_values_at(self):
        names = [value.__data__["__meta__"]["name"] for value in self.dt_USA.values_at(0)]
        names.sort()
        names == ["United State", ]

        names = [value.__data__["__meta__"]["name"] for value in self.dt_USA.values_at(1)]
        names.sort()
        names == ["Maryland", "Virginia"]

        zipcodes = [
            value.__data__["__meta__"]["zipcode"]
            for value in self.dt_USA.values_at(2)
        ]
        zipcodes.sort()
        zipcodes == ["20030", "20740", "20878", "22202"]

    def test_items_at(self):
        keys = [key for key, value in self.dt_USA.items_at(0)]
        keys.sort()
        assert keys == ["__root__"]

        keys = [key for key, value in self.dt_USA.items_at(1)]
        keys.sort()
        assert keys == ["MD", "VA"]

        keys = [key for key, value in self.dt_USA.items_at(2)]
        keys.sort()
        assert keys == ["Arlington", "College Park", "Fairfax", "Gaithersburg"]

    def test_length_at(self):
        assert self.dt_USA.length_at(0) == 1
        assert self.dt_USA.length_at(1) == 2
        assert self.dt_USA.length_at(2) == 4

    def test_mutable(self):
        """

        **中文文档**

        测试对子树的修改, 是不是也会修改母树。(因为都是Mutable的对象, 所以应该会)
        """
        usa = DictTree(name="USA", pop=200 * 10 ** 6)  # 创建母树
        usa["VA"] = DictTree(name="VA", pop=3 * 10 ** 6)  # 创建子树
        dt = usa["VA"]  # 获取子树
        dt.pop = 999999  # 修改子树的属性

        # 看是否也修改了母树的__data__
        assert usa.__data__["VA"]["__meta__"]["pop"] == 999999

    def test_stats_at(self):
        result = self.dt_USA.stats()

        assert result[0]["depth"] == 0
        assert result[0]["leaf"] == 0
        assert result[0]["root"] == 1

        assert result[1]["depth"] == 1
        assert result[1]["leaf"] == 0
        assert result[1]["root"] == 2

        assert result[2]["depth"] == 2
        assert result[2]["leaf"] == 4
        assert result[2]["root"] == 0


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
