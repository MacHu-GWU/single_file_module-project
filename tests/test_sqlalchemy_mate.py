#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import time
import random
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import Integer, String
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
metadata.create_all(engine)
ins = t_test.insert()


def test_smart_insert():
    """
    
    **中文文档**
    
    测试smart_insert的基本功能, 以及与普通的insert比较性能。
    """
    # Smart Insert
    engine.execute(t_test.delete())

    data = [{"id": random.randint(1, 10000)} for i in range(20)]
    for row in data:
        try:
            engine.execute(ins, row)
        except IntegrityError:
            pass
    assert 15 <= count_n_rows(engine, t_test) <= 20

    data = [{"id": i} for i in range(1, 1 + 10000)]
    
    st = time.clock()
    smart_insert(engine, t_test, data, 5)
    elapse1 = time.clock() - st
    
    assert count_n_rows(engine, t_test) == 10000
    
    # Regular Insert
    engine.execute(t_test.delete())

    data = [{"id": random.randint(1, 10000)} for i in range(20)]
    for row in data:
        try:
            engine.execute(ins, row)
        except IntegrityError:
            pass
    assert 15 <= count_n_rows(engine, t_test) <= 20

    data = [{"id": i} for i in range(1, 1 + 10000)]
    
    st = time.clock()
    for row in data:
        try:
            engine.execute(ins, row)
        except IntegrityError:
            pass
    elapse2 = time.clock() - st
    
    assert count_n_rows(engine, t_test) == 10000

    assert elapse1 * 5 < elapse2


def test_count_row():
    engine.execute(t_test.delete())
    engine.execute(t_test.insert(), [{"id": 1}, {"id": 2}, {"id": 3}])
    assert sm.count_row(engine, t_test) == 3
    
    
def test_select_column():
    engine.execute(t_test.delete())
    engine.execute(t_test.insert(), [{"id": 1}, {"id": 2}, {"id": 3}])
    id_list = sm.select_column(engine, t_test.c.id)
    assert id_list == [1, 2, 3]
        

if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
