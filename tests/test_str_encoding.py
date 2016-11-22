#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])