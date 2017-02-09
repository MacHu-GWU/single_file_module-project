#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
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


def test_compress_decompress():
    s = \
    """
    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    """

    s1 = str_encoding.compress_str(s)
    assert len(s1) < len(s)
    assert s == str_encoding.decompress_str(s1)
    

if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])