# -*- coding: utf-8 -*-

import pytest
from sfm import ziplib

s = """
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
""".strip()

obj_byte = s.encode("utf-8")
obj_str = s
obj_dict = dict(content=s)


def test_compress():
    # compress bytes, string, and dict
    #   return type = bytes
    ziplib.compress(obj_byte, return_type="bytes")
    ziplib.compress(obj_str, return_type="bytes")
    ziplib.compress(obj_dict, return_type="bytes")

    #   return type = str
    ziplib.compress(obj_byte, return_type="str")
    ziplib.compress(obj_str, return_type="str")
    ziplib.compress(obj_dict, return_type="str")

    # decompress
    #   recover obj
    assert obj_dict == ziplib.decompress(
        ziplib.compress(obj_dict, return_type="bytes"),
        return_type="obj",
    )

    assert obj_dict == ziplib.decompress(
        ziplib.compress(obj_dict, return_type="str"),
        return_type="obj",
    )

    #   recover str
    assert obj_str == ziplib.decompress(
        ziplib.compress(obj_str, return_type="bytes"),
        return_type="str",
    )

    assert obj_str == ziplib.decompress(
        ziplib.compress(obj_str, return_type="str"),
        return_type="str",
    )

    #   recover byte
    assert obj_byte == ziplib.decompress(
        ziplib.compress(obj_byte, return_type="bytes"),
        return_type="bytes",
    )

    assert obj_byte == ziplib.decompress(
        ziplib.compress(obj_byte, return_type="str"),
        return_type="bytes",
    )

    obj2_after = ziplib.compress(obj_str, return_type="str")
    assert len(obj2_after) < len(obj_str)  # size is reduced


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
