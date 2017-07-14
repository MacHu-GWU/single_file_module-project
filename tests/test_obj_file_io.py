#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import pytest
import pickle
import functools
from sfm.obj_file_io import dump_func, safe_dump_func, load_func


@dump_func
def dump(obj):
    return pickle.dumps(obj)


@safe_dump_func
def safe_dump(obj):
    return pickle.dumps(obj)


@load_func
def load(b):
    return pickle.loads(b)


def test_dump_safe_dump_load():
    obj = dict(a=1, b=2, c=3)

    b = dump(obj, "data.pk", verbose=True)
    b = safe_dump(obj, "data.pk", verbose=True)
    obj1 = load("data.pk", verbose=True)
    assert obj == obj1

    b = dump(obj, "data.pk.gz", compress=True, verbose=True)
    b = safe_dump(obj, "data.pk.gz", compress=True, verbose=True)
    obj2 = load("data.pk.gz", decompress=True, verbose=True)
    assert obj == obj2

    # temp file will be removed in 20 seconds
    time.sleep(20.0)
    for p in ["data.pk", "data.pk.gz"]:
        try:
            os.remove(p)
        except:
            pass


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
