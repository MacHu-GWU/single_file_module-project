# -*- coding: utf-8 -*-

from __future__ import print_function
import pytest
from sfm.fingerprint import fingerprint
from six import integer_types, string_types


def test_md5_file():
    a_file = __file__.replace("test_fingerprint.py", "all.py")

    id1 = fingerprint.of_file(a_file)
    id2 = fingerprint.of_file(a_file, nbytes=1000)
    id3 = fingerprint.of_file(a_file, chunk_size=1)
    id4 = fingerprint.of_file(a_file, chunk_size=2)
    assert id1 == id2 == id3 == id4

    id1 = fingerprint.of_file(a_file, nbytes=5)
    id2 = fingerprint.of_file(a_file, nbytes=5, chunk_size=2)
    id3 = fingerprint.of_file(a_file, nbytes=5, chunk_size=1)
    assert id1 == id2 == id3

    with pytest.raises(ValueError) as exc_info:
        fingerprint.of_file(a_file, nbytes=-1)

    with pytest.raises(ValueError) as exc_info:
        fingerprint.of_file(a_file, chunk_size=0)


def test_hash_anything():
    """This test may failed in different operation system.
    """
    a_bytes = bytes(123)
    md5 = fingerprint.of_bytes(a_bytes)
    assert isinstance(md5, string_types)

    a_text = "Hello World!"
    md5 = fingerprint.of_bytes(a_bytes)
    assert isinstance(md5, string_types)

    a_pyobj = {"key": "value"}
    md5 = fingerprint.of_pyobj(a_pyobj)
    assert isinstance(md5, string_types)

    fingerprint.set_return_int()
    assert isinstance(fingerprint.of_text(a_text), integer_types)
    fingerprint.set_return_str()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
