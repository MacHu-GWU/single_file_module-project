#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module extend the power of mongoengine.
"""

import math
import random
import mongoengine
from collections import OrderedDict
from copy import deepcopy


def grouper_list(l, n):
    """Evenly divide list into fixed-length piece, no filled value if chunk
    size smaller than fixed-length.

    Example::

        >>> list(grouper(range(10), n=3)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    **中文文档**

    将一个列表按照尺寸n, 依次打包输出, 有多少输出多少, 并不强制填充包的大小到n。

    下列实现是按照性能从高到低进行排列的:

    - 方法1: 建立一个counter, 在向chunk中添加元素时, 同时将counter与n比较, 如果一致
      则yield。然后在最后将剩余的item视情况yield。
    - 方法2: 建立一个list, 每次添加一个元素, 并检查size。
    - 方法3: 调用grouper()函数, 然后对里面的None元素进行清理。
    """
    chunk = list()
    counter = 0
    for item in l:
        counter += 1
        chunk.append(item)
        if counter == n:
            yield chunk
            chunk = list()
            counter = 0
    if len(chunk) > 0:
        yield chunk


class ExtendedDocument(mongoengine.Document):

    """Provide `mongoengine.Document <http://docs.mongoengine.org/apireference.html#mongoengine.Document>`_
    more utility methods.

    **中文文档**

    为默认的 ``mongoengine.Document`` 提供了更多的便捷方法。
    """
    meta = {
        "abstract": True,
    }

    def keys(self):
        """Convert to field list.
        """
        try:
            return list(self._fields_ordered)
        except AttributeError:
            raise TypeError("It does not inherit from mongoengine.Document!")

    def values(self):
        """Convert to field value list.
        """
        return [self._data.get(attr) for attr in self.keys()]

    def items(self):
        """Convert to field and value pair list.
        """
        return [(attr, self._data.get(attr)) for attr in self.keys()]

    def to_tuple(self):
        """Convert to field tuple.
        """
        return self._fields_ordered

    def to_list(self):
        """Convert to field list.
        """
        return self.keys()

    def to_dict(self):
        """Convert to dict.
        """
        return dict(self.items())

    def to_OrderedDict(self):
        """Convert to OrderedDict.
        """
        return OrderedDict(self.items())

    def __repr__(self):
        kwargs = list()
        for attr, value in self.items():
            kwargs.append("%s=%r" % (attr, value))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(kwargs))

    def __str__(self):
        return self.__repr__()

    def absorb(self, other):
        """For attributes of others that value is not None, assign it to self.

        **中文文档**

        将另一个文档中的数据更新到本条文档。当且仅当数据值不为None时。
        """
        if not isinstance(other, self.__class__):
            raise TypeError

        for attr, value in other.items():
            if value is not None:
                setattr(self, attr, deepcopy(value))

    def revise(self, data):
        """Revise attributes value with dictionary data.

        **中文文档**

        将一个字典中的数据更新到本条文档。当且仅当数据值不为None时。
        """
        if not isinstance(data, dict):
            raise TypeError

        for key, value in data.items():
            if value is not None:
                setattr(self, key, deepcopy(value))

    @classmethod
    def collection(cls):
        """Get pymongo Collection instance.

        **中文文档**

        获得pymongo.Collection的实例。
        """
        return cls._get_collection()

    @classmethod
    def col(cls):
        """Get pymongo Collection instance.

        **中文文档**

        获得pymongo.Collection的实例。
        """
        return cls._get_collection()

    @classmethod
    def smart_insert(cls, data, minimal_size=5):
        """An optimized Insert strategy.

        **中文文档**

        在Insert中, 如果已经预知不会出现IntegrityError, 那么使用Bulk Insert的速度要
        远远快于逐条Insert。而如果无法预知, 那么我们采用如下策略:

        1. 尝试Bulk Insert, Bulk Insert由于在结束前不Commit, 所以速度很快。
        2. 如果失败了, 那么对数据的条数开平方根, 进行分包, 然后对每个包重复该逻辑。
        3. 若还是尝试失败, 则继续分包, 当分包的大小小于一定数量时, 则使用逐条插入。
          直到成功为止。

        该Insert策略在内存上需要额外的 sqrt(nbytes) 的开销, 跟原数据相比体积很小。
        但时间上是各种情况下平均最优的。
        """
        if isinstance(data, list):
            # 首先进行尝试bulk insert
            try:
                cls.objects.insert(data)
            # 失败了
            except mongoengine.NotUniqueError:
                # 分析数据量
                n = len(data)
                # 如果数据条数多于一定数量
                if n >= minimal_size ** 2:
                    # 则进行分包
                    n_chunk = math.floor(math.sqrt(n))
                    for chunk in grouper_list(data, n_chunk):
                        cls.smart_insert(chunk, minimal_size)
                # 否则则一条条地逐条插入
                else:
                    for document in data:
                        try:
                            cls.objects.insert(document)
                        except mongoengine.NotUniqueError:
                            pass
        else:
            try:
                cls.objects.insert(data)
            except mongoengine.NotUniqueError:
                pass

    @classmethod
    def by_id(cls, _id):
        """Get one instance by _id.

        **中文文档**

        根据_id, 返回一条文档。
        """
        return cls.objects(__raw__={"_id": _id}).get()

    @classmethod
    def by_filter(cls, filters):
        """Filter objects by pymongo dict query.

        **中文文档**

        使用pymongo的API进行query。
        """
        return cls.objects(__raw__=filters)

    @classmethod
    def random_sample(cls, filters=None, n=5):
        """

        **中文文档**

        从collection中随机选择 ``n`` 个样本。
        """
        data = list()

        id_field = cls._meta["id_field"]

        if filters is None:
            pipeline = [{"$sample": {"size": n}}]
            col = cls.col()

            if id_field == "_id":
                for doc in col.aggregate(pipeline):
                    obj = cls(**doc)
                    data.append(obj)

            else:
                for doc in col.aggregate(pipeline):
                    doc[id_field] = doc["_id"]
                    del doc["_id"]
                    obj = cls(**doc)
                    data.append(obj)
        else:
            if id_field == "_id":
                for doc in random.sample(list(cls.col().find(filters)), n):
                    obj = cls(**doc)
                    data.append(obj)
            else:
                filters["_id"] = filters[id_field]
                del filters[id_field]
                for doc in random.sample(list(cls.col().find(filters)), n):
                    doc[id_field] = doc["_id"]
                    del doc["_id"]
                    obj = cls(**doc)
                    data.append(obj)

        return data


#--- Unittest ---
class User(ExtendedDocument):
    user_id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField()

    meta = {"collection": "user"}


if __name__ == "__main__":
    import mongoengine

    mongoengine.connect()


def test_smart_insert():
    import time
    import random

    # Smart Insert
    User.objects.delete()

    users = set([User(user_id=random.randint(1, 10000)) for i in range(20)])
    User.objects.insert(users)
    assert 15 <= User.objects.count() <= 20

    users = [User(user_id=i) for i in range(1, 1 + 10000)]

    st = time.clock()
    User.smart_insert(users)
    elapse1 = time.clock() - st

    assert User.objects.count() == 10000  # after smart insert, we got 10000 doc

    # Regular Insert
    User.objects.delete()

    users = set([User(user_id=random.randint(1, 10000)) for i in range(20)])
    User.objects.insert(users)
    assert 15 <= User.objects.count() <= 20

    users = [User(user_id=i) for i in range(1, 1 + 10000)]

    st = time.clock()
    for user in users:
        try:
            user.save()
        except:
            pass
    elapse2 = time.clock() - st

    assert User.objects.count() == 10000  # after regular insert, we got 10000 doc

    assert elapse1 <= elapse2


def test_query():
    User(user_id=1, name="Jack").save()
    User(user_id=2, name="Tom").save()

    assert User.by_id(1).name == "Jack"
    assert User.by_filter({"_id": 2})[:][0].name == "Tom"


def test_random_sample():
    User.col().remove({})
    for i in range(1000):
        user = User(user_id=i)
        user.save()

    assert len(User.random_sample(n=3)) == 3
    for user in User.random_sample(filters={"user_id": {"$gte": 500}}, n=3):
        assert user.user_id >= 500


if __name__ == "__main__":
    #
    test_smart_insert()
    test_query()
    test_random_sample()
