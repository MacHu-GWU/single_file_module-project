#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
import string
import pytest
from sfm import str_encoding


def test_base64_urlsafe():
    for before in [
        r"C:\windows",
        "a_b_c!@#$%^&*()",
        "中文英文日文",
    ]:
        after = str_encoding.encode_base64_urlsafe(before)
        assert before == str_encoding.decode_base64_urlsafe(after)


def test_hexstr():
    for before in [
        r"C:\windows",
        "a_b_c!@#$%^&*()",
        "中文英文日文",
    ]:
        after = str_encoding.encode_hexstr(before)
        assert before == str_encoding.decode_hexstr(after)

    s = "中文英文日文"
    s1 = str_encoding.encode_hexstr(s)
    assert len(set(s1).difference("0123456789abcdef")) == 0
    
    
if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
