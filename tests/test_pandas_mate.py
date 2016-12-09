#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import warnings
import pytest
import numpy as np, pandas as pd
from sfm import pandas_mate
from sfm import rnd
from sfm.timer import Timer, EasyTimer

data_file_path = __file__.replace("test_pandas_mate.py", "matrix.csv")

def create_data_file():
    if not os.path.exists(data_file_path):
        n_rows = 10000
        df = pd.DataFrame(np.random.randint(1, 100, (n_rows, 2)), columns=list("AB"))
        df.to_csv(data_file_path, index=False)

create_data_file()


def test_csv_tuple_iterator():
    timer = EasyTimer()
    
    timer.start()
    for a, b in pandas_mate.IOTool.csv_tuple_iterator(
        data_file_path, chunksize=1000000):
        pass
    timer.stop()
    elapse1 = timer.elapsed
    
    timer.start()
    for index, a, b in pd.read_csv(data_file_path).itertuples():
        pass
    timer.stop()
    elapse2 = timer.elapsed
    
    if not elapse1 < elapse2:
        warnings.warn("IOTool.csv_tuple_iterator is slower than itertuples()!")
    


class TestTransform():
    def test_key_row_table(self):
        nrows = 1000
        df = pd.DataFrame()
        df["id"] = [rnd.rand_hexstr(32) for i in range(nrows)]
        df["value"] = np.random.randint(1, 100, nrows)
        df.index = df["id"]
        
        with Timer(display=False) as timer:
            table = pandas_mate.Transform.key_row_table(df)
            for ind in df.index:
                row = table[ind]
        elapse1 = timer.elapsed
        
        with Timer(display=False) as timer:
            for ind, row in df.iterrows():
                pass
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
    