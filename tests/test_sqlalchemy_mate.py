#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import pytest
import time
import random
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import Integer, String
from sqlalchemy import select
from sfm.sqlalchemy_mate import smart_insert
from sfm import sqlalchemy_mate as sm


def count_n_rows(engine, table):
    """Count how many row in a table.
    """
    return engine.execute(table.count()).fetchone()[0]


engine = create_engine("sqlite:///:memory:")
metadata = MetaData()

t_test = Table("test", metadata,
               Column("id", Integer, primary_key=True),
               )

t_item = Table("item", metadata,
               Column("store_id", Integer, primary_key=True),
               Column("item_id", Integer, primary_key=True),
               )

t_user = Table("user", metadata,
               Column("user_id", Integer, primary_key=True),
               Column("name", String),
               )

metadata.create_all(engine)
ins = t_test.insert()


def test_smart_insert():
    """

    **中文文档**

    测试smart_insert的基本功能, 以及与普通的insert比较性能。
    """
    n = 10000
    # Smart Insert
    engine.execute(t_test.delete())

    data = [{"id": random.randint(1, n)} for i in range(20)]
    for row in data:
        try:
            engine.execute(ins, row)
        except IntegrityError:
            pass
    assert 15 <= count_n_rows(engine, t_test) <= 20

    data = [{"id": i} for i in range(1, 1 + n)]

    st = time.clock()
    smart_insert(engine, t_test, data, 5)
    elapse1 = time.clock() - st

    assert count_n_rows(engine, t_test) == n

    # Regular Insert
    engine.execute(t_test.delete())

    data = [{"id": random.randint(1, n)} for i in range(20)]
    for row in data:
        try:
            engine.execute(ins, row)
        except IntegrityError:
            pass
    assert 15 <= count_n_rows(engine, t_test) <= 20

    data = [{"id": i} for i in range(1, 1 + n)]

    st = time.clock()
    for row in data:
        try:
            engine.execute(ins, row)
        except IntegrityError:
            pass
    elapse2 = time.clock() - st

    assert count_n_rows(engine, t_test) == n

    if n >= 10000:
        assert elapse1 * 5 < elapse2
    else:
        assert elapse1 < elapse2


def test_count_row():
    engine.execute(t_test.delete())
    engine.execute(t_test.insert(), [{"id": 1}, {"id": 2}, {"id": 3}])
    assert sm.count_row(engine, t_test) == 3


def test_select_column():
    engine.execute(t_user.delete())
    engine.execute(t_user.insert(), [{"user_id": 1, "name": "Jack"},
                                     {"user_id": 2, "name": "Mike"},
                                     {"user_id": 3, "name": "Paul"}])
    header, user_id_list = sm.select_column(engine, t_user.c.user_id)
    assert header == "user_id"
    assert user_id_list == [1, 2, 3]

    headers, data = sm.select_column(engine, t_user.c.user_id, t_user.c.name)
    assert headers == ["user_id", "name"]
    assert data == [(1, "Jack"), (2, "Mike"), (3, "Paul")]


def test_select_distinct_column():
    engine.execute(t_test.delete())
    engine.execute(t_test.insert(), [{"id": 1}, {"id": 2}, {"id": 3}])

    engine.execute(t_item.delete())
    engine.execute(t_item.insert(), [{"store_id": 1, "item_id": 1},
                                     {"store_id": 1, "item_id": 2},
                                     {"store_id": 2, "item_id": 1},
                                     {"store_id": 2, "item_id": 2}])

    assert sm.select_distinct_column(engine, t_test.c.id) == [1, 2, 3]

    assert sm.select_distinct_column(
        engine, t_item.c.store_id, t_item.c.item_id) == [
            [1, 1], [1, 2], [2, 1], [2, 2]]


def test_table_to_csv():
    engine.execute(t_test.delete())
    engine.execute(t_test.insert(), [{"id": i + 1} for i in range(10)])
    
    filepath = __file__.replace("test_sqlalchemy_mate.py", "t_test.csv")
    sm.table_to_csv(t_test, engine, filepath, chunksize=1)
        

def test_sql_to_pretty_table():
    sql = select([t_test])
    pretty_table = sm.sql_to_pretty_table(sql, engine)
    print(pretty_table)
    
    
if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
