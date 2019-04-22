# -*- coding: utf-8 -*-

import pytest
import json
import pickle
from sfm.obj_file_io import dump_func, load_func
from pathlib_mate import Path

here = Path(__file__).parent

data_pk = here.append_parts("data.pk").abspath
data_pk_gz = here.append_parts("data.pk.gz").abspath
data_js = here.append_parts("data.json").abspath
data_js_gz = here.append_parts("data.json.gz").abspath


def teardown_module(module):
    """teardown any state that was previously setup with a setup_module
    method.
    """
    import os
    import time

    # temp file will be removed soon
    time.sleep(1.0)

    for p in [data_pk, data_pk_gz, data_js, data_js_gz]:
        try:
            os.remove(p)
        except:
            pass


@dump_func(serializer_type="binary")
def dump_pk(obj):
    return pickle.dumps(obj)


@load_func(serializer_type="binary")
def load_pk(b):
    return pickle.loads(b)


@dump_func(serializer_type="str")
def dump_js(obj):
    return json.dumps(obj, ensure_ascii=False)


@load_func(serializer_type="str")
def load_js(s):
    return json.loads(s)


def test_dump_safe_dump_load():
    obj = dict(a=1, b=2, c=3)

    b = dump_pk(obj, data_pk, verbose=True)
    obj1 = load_pk(data_pk, verbose=True)
    assert obj == obj1

    b = dump_pk(obj, data_pk_gz, compress=True, verbose=True)
    obj2 = load_pk(data_pk_gz, decompress=True, verbose=True)
    assert obj == obj2

    s = dump_js(obj, data_js, verbose=True)
    obj1 = load_js(data_js, verbose=True)
    assert obj == obj1

    b = dump_js(obj, data_js_gz, compress=True, verbose=True)
    obj2 = load_js(data_js_gz, decompress=True, verbose=True)
    assert obj == obj2


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
