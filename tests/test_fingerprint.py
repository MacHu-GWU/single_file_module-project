#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import platform
import pytest
from sfm.fingerprint import is_py2, fingerprint
from sfm.packages.six import integer_types

def test_md5_file():
    a_file = __file__.replace("test_fingerprint.py", "test_all.py")
    
    SYS_NAME = platform.system()
    if SYS_NAME == "Windows":
        assert fingerprint.of_file(a_file) == "b8a17e5c1927a21a95263fccbf0af7d4"
        assert fingerprint.of_file(a_file, nbytes=1000) == "b8a17e5c1927a21a95263fccbf0af7d4"
        assert fingerprint.of_file(a_file, chunk_size=1) == "b8a17e5c1927a21a95263fccbf0af7d4"
        assert fingerprint.of_file(a_file, chunk_size=2) == "b8a17e5c1927a21a95263fccbf0af7d4"
    
        assert fingerprint.of_file(a_file, nbytes=5) == "f35b4f5a273e9c6ce1fd034c562b4ff4"
        assert fingerprint.of_file(a_file, nbytes=5, chunk_size=1) == "f35b4f5a273e9c6ce1fd034c562b4ff4"
        assert fingerprint.of_file(a_file, nbytes=5, chunk_size=2) == "f35b4f5a273e9c6ce1fd034c562b4ff4"
        
        with pytest.raises(ValueError) as exc_info:
            fingerprint.of_file(a_file, nbytes=-1)
            
        with pytest.raises(ValueError) as exc_info:
            fingerprint.of_file(a_file, chunk_size=0)


def test_hash_anything():
    """This test may failed in different operation system.
    """
    a_bytes = bytes(123)
    md5 = fingerprint.of_bytes(a_bytes)
    print(md5)
    
    a_text = "Hello World!"
    md5 = fingerprint.of_bytes(a_bytes)
    print(md5)
    
    a_pyobj = {"key": "value"}
    md5 = fingerprint.of_pyobj(a_pyobj)
    print(md5)

    fingerprint.set_return_int()
    assert isinstance(fingerprint.of_text(a_text), integer_types)


if __name__ == "__main__":
    import py
    import os
    py.test.cmdline.main("%s --tb=native -s" % os.path.basename(__file__))
