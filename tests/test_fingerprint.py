#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from sfm.fingerprint import is_py2, fingerprint
from sfm.packages.six import integer_types


def test_hash_anything():
    """This test may failed in different operation system.
    """
    a_bytes = bytes(123)
    a_text = "Hello World!"
    a_pyobj = {"key": "value"}
    a_file = __file__.replace("test_fingerprint.py", "test_all.py")

    print(fingerprint.of_bytes(a_bytes))
    print(fingerprint.of_text(a_text))
    print(fingerprint.of_pyobj(a_pyobj))
    print(fingerprint.of_file(a_file))

    fingerprint.set_return_int()
    assert isinstance(fingerprint.of_text(a_text), integer_types)


if __name__ == "__main__":
    import py
    import os
    py.test.cmdline.main("%s --tb=native -s" % os.path.basename(__file__))
