#!/usr/bin/env python
# -*- coding: utf-8 -*-

#--- Unittest ---
import time
import random
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import Integer
from sfm.sqlalchemy_mate import smart_insert


def count_n_rows(engine, table):
    """Count how many row in a table.
    """
    return engine.execute(table.count()).fetchone()[0]


engine = create_engine("sqlite:///:memory:")
metadata = MetaData()
t_test = Table("test", metadata,
               Column("id", Integer, primary_key=True),
               )
metadata.create_all(engine)
ins = t_test.insert()


def test_smart_insert():
    """
    
    **中文文档**
    
    测试smart_insert的基本功能和性能
    """
    engine.execute(t_test.delete())

    data = [{"id": random.randint(1, 10000)} for i in range(20)]
    for row in data:
        try:
            engine.execute(ins, row)
        except IntegrityError:
            pass
    assert 15 <= count_n_rows(engine, t_test) <= 20

    data = [{"id": i} for i in range(1, 10001)]
    st = time.clock()
    smart_insert(engine, t_test, data, 5)
    elapse = time.clock() - st
    assert count_n_rows(engine, t_test) == 10000

    print("Smart insert elapse: %.6f." % elapse)


def test_regular_insert():
    """
    
    **中文文档**
    
    测试普通insert与smart insert在复杂情况下相比的性能
    """
    engine.execute(t_test.delete())

    data = [{"id": random.randint(1, 10000)} for i in range(20)]
    for row in data:
        try:
            engine.execute(ins, row)
        except IntegrityError:
            pass
    assert 15 <= count_n_rows(engine, t_test) <= 20

    data = [{"id": i} for i in range(1, 10001)]
    st = time.clock()
    for row in data:
        try:
            engine.execute(ins, row)
        except IntegrityError:
            pass
    elapse = time.clock() - st
    assert count_n_rows(engine, t_test) == 10000

    print("Regular insert elapse: %.6f." % elapse)


if __name__ == "__main__":
    import py
    import os
    py.test.cmdline.main("%s --tb=native -s" % os.path.basename(__file__))
