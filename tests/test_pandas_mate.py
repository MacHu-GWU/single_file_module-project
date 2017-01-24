#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import warnings
import pytest
import numpy as np
import pandas as pd
from sfm import pandas_mate
from sfm import rnd
from sfm.timer import Timer, EasyTimer

data_file_path = __file__.replace("test_pandas_mate.py", "matrix.csv")


def create_data_file():
    if not os.path.exists(data_file_path):
        n_rows = 10000
        df = pd.DataFrame(
            np.random.randint(1, 100, (n_rows, 2)), columns=list("AB"))
        df.to_csv(data_file_path, index=False)

create_data_file()


class TestIOTool:

    def test_iterate_tuple_from_csv(self):
        display = True

        with Timer(display=display) as timer1:
            for index, a, b in pd.read_csv(data_file_path).itertuples():
                pass

        with Timer(display=display) as timer2:
            for a, b in pandas_mate.IOTool.iterate_tuple_from_csv(
                    data_file_path, iterator=True, chunksize=100):
                pass

        with Timer(display=display) as timer3:
            for a, b in pandas_mate.IOTool.iterate_tuple_from_csv(
                    data_file_path, nrows=100):
                pass

        if not timer1.elapsed < timer3.elapsed:
            warnings.warn(
                "IOTool.iterate_tuple_from_csv() is slower than itertuples()!")

    def test_index_row_map_from_csv(self):
        display = False

        with Timer(display=display) as timer:
            table1 = pandas_mate.IOTool.index_row_map_from_csv(
                data_file_path, index_col="A")

        with Timer(display=display) as timer:
            table2 = pandas_mate.IOTool.index_row_map_from_csv(
                data_file_path, index_col="A", iterator=True, chunksize=100)


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


@pytest.fixture(scope="module")
def teardown(request):
    try:
        os.remove(data_file_path)
    except:
        pass


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
