#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import warnings
from datetime import datetime
import pytest
import numpy as np
import pandas as pd
from sfm import pandas_mate
from sfm import rnd
from sfm.timer import Timer, EasyTimer

data_file_path = __file__.replace("test_pandas_mate.py", "matrix.csv")


def create_data_file():
    if not os.path.exists(data_file_path):
        n_rows = 1000
        df = pd.DataFrame()
        df["_id"] = [rnd.rand_hexstr(32) for i in range(n_rows)]
        df["a"] = np.random.randint(1, 1000, n_rows)
        df["b"] = np.random.random(n_rows)
        df.to_csv(data_file_path, index=False)

create_data_file()


def test_itertuple():
    display = False
    
    df = pd.read_csv(data_file_path)
    
    with Timer(display=display, title="DataFrame.itertuples()") as timer1:
        for _id, a, b in df.itertuples(index=False):
            pass
    
    with Timer(display=display, title="itertuples()") as timer2:
        for _id, a, b in pandas_mate.itertuple(df):
            pass
        
    if not timer2.elapsed < timer1.elapsed:
        warnings.warn("DataFrame.itertuples() should not faster than itertuples(df)!")
        

class TestIOTool:

    def test_iterate_tuple_from_csv(self):
        display = False

        with Timer(display=display) as timer1:
            for _id, a, b  in pd.read_csv(data_file_path).itertuples(index=False):
                pass

        with Timer(display=display) as timer2:
            for _id, a, b in pandas_mate.IOTool.iterate_tuple_from_csv(
                    data_file_path, iterator=True, chunksize=100):
                pass

        with Timer(display=display) as timer3:
            for _id, a, b in pandas_mate.IOTool.iterate_tuple_from_csv(
                    data_file_path):
                pass

        if not timer1.elapsed < timer3.elapsed:
            warnings.warn(
                "IOTool.iterate_tuple_from_csv() is slower than itertuples()!")

    def test_index_row_map_from_csv(self):
        display = False

        with Timer(display=display) as timer:
            table1 = pandas_mate.IOTool.index_row_map_from_csv(
                data_file_path, index_col="_id")

        with Timer(display=display) as timer:
            table2 = pandas_mate.IOTool.index_row_map_from_csv(
                data_file_path, index_col="_id", iterator=True, chunksize=100)

    def test_to_sql_smart_insert(self):
        import random
        import sqlalchemy
        from sqlalchemy import create_engine, MetaData, Table, Column
        from sqlalchemy import String, Integer, Float
        
        def count_n_rows(engine, table):
            """Count how many row in a table.
            """
            return engine.execute(table.count()).fetchone()[0]
        
        engine = create_engine("sqlite:///:memory:")
        metadata = MetaData()
        t_test = Table(
            "test", metadata,
            Column("_id", String, primary_key=True),
            Column("a", Integer),
            Column("b", Float),
        )
        metadata.create_all(engine)
        
        df = pd.read_csv(data_file_path)
        
        rows = list(pandas_mate.Transform.index_row_map(df).values())
        data = random.sample(rows, 5)
        engine.execute(t_test.insert(), data)
        
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            df.to_sql("test", engine, index=False, if_exists="append")
        assert count_n_rows(engine, t_test) == 5
        
        pandas_mate.IOTool.to_sql_smart_insert(df, t_test, engine)
        assert count_n_rows(engine, t_test) == 1000


class TestTransform(object):

    def test_index_row_map(self):
        display = False

        nrows = 1000
        df = pd.DataFrame()
        df["id"] = [rnd.rand_hexstr(32) for i in range(nrows)]
        df["value"] = np.random.randint(1, 100, nrows)
        df.index = df["id"]

        with Timer(display=display) as timer:
            table = pandas_mate.Transform.index_row_map(df)
            for ind in df.index:
                row = table[ind]
        elapse1 = timer.elapsed

        with Timer(display=display) as timer:
            table = dict()
            for ind, row in df.iterrows():
                table[ind] = dict(row)
        elapse2 = timer.elapsed

        if not elapse1 < elapse2:
            warnings.warn("Transform.key_row_table is slower than iterrows()!")

    def test_grouper_df(self):
        df = pd.DataFrame(np.random.random((10, 4)))
        df1, df2, df3, df4 = list(pandas_mate.Transform.grouper_df(df, 3))
        for df_ in [df1, df2, df3]:
            assert df_.shape == (3, 4)
        assert df4.shape == (1, 4)

    def test_generic_python_dict_list(self):
        data = [
            ["Jack", 1, 0.1, None],
            ["Tom", 2, None, datetime(2000, 1, 2)],
            ["Bob", None, 0.3, datetime(2000, 1, 3)],
            [None, 4, 0.4, datetime(2000, 1, 4)],
        ]
        df = pd.DataFrame(data, columns=list("ABCD"))
        data = pandas_mate.Transform.generic_python_dict_list(df, int_col="B")
        doc1, doc2, doc3, doc4 = data
        assert doc1["D"] == None
        assert doc2["C"] == None
        assert doc3["B"] == None
        assert doc4["A"] == None
        
        assert doc1["B"] == 1
        assert doc2["B"] == 2
        assert doc4["B"] == 4
        
        assert doc2["D"].day == 2
        assert doc3["D"].day == 3
        assert doc4["D"].day == 4


def teardown_module():
    try:
        os.remove(data_file_path)
    except:
        pass


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
