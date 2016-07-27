#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sfm.fingerprint import is_py2, fingerprint
from sfm.packages.six import integer_types


def test_hash_anything():
    a_bytes = bytes(123)
    a_text = "Hello World!"
    a_pyobj = {"key": "value"}
    a_file = __file__.replace("test_fingerprint.py", "test_all.py")

    if is_py2:
        assert fingerprint.of_bytes(
            a_bytes) == "202cb962ac59075b964b07152d234b70"
        assert fingerprint.of_text(
            a_text) == "ed076287532e86365e841e92bfc50d8c"
        assert fingerprint.of_pyobj(
            a_pyobj) == "3a99ab89f2010f8b59c8455b320a2e17"
        assert fingerprint.of_file(
            a_file) == "b8a17e5c1927a21a95263fccbf0af7d4"
    else:
        assert fingerprint.of_bytes(
            a_bytes) == "b1fec41621e338896e2d26f232a6b006"
        assert fingerprint.of_text(
            a_text) == "ed076287532e86365e841e92bfc50d8c"
        assert fingerprint.of_pyobj(
            a_pyobj) == "4c502ab399c89c8758a2d8c37be98f69"
        assert fingerprint.of_file(
            a_file) == "b8a17e5c1927a21a95263fccbf0af7d4"

    fingerprint.set_return_int()
    assert isinstance(fingerprint.of_text(a_text), integer_types)


if __name__ == "__main__":
    import py
    import os
    py.test.cmdline.main("%s --tb=native -s" % os.path.basename(__file__))
