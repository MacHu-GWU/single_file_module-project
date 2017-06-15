#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import pytest
import pickle
import functools
from sfm.obj_file_io import _dump, _safe_dump, _load


def pickle_dumper(obj):
    return pickle.dumps(obj)


def pickle_loader(b):
    return pickle.loads(b)


def test_dumper_loader():
    obj = dict(a=1, b=2)
    b = pickle_dumper(obj)
    obj = pickle_loader(b)


def test_partial():
    dump = functools.partial(_dump, dumper_func=pickle_dumper)
    safe_dump = functools.partial(_safe_dump, dumper_func=pickle_dumper)
    load = functools.partial(_load, loader_func=pickle_loader)

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
