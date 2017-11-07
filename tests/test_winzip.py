#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
from sfm import winzip


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    import time

    # temp file will be removed soon
    time.sleep(1.0)
    for p in ["1.zip", "2.zip", "3.zip"]:
        try:
            os.remove(p)
        except:
            pass


def test_winzip():
    winzip.zip_a_folder(os.getcwd(), "1.zip")
    winzip.zip_everything_in_a_folder(os.getcwd(), "2.zip")
    winzip.zip_many_files([__file__, ], "3.zip")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
