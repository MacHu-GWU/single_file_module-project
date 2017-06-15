#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import pytest
from sfm import winzip


def test_winzip():
    winzip.zip_a_folder(os.getcwd(), "1.zip")
    winzip.zip_everything_in_a_folder(os.getcwd(), "2.zip")
    winzip.zip_many_files([__file__, ], "3.zip")

    # temp file will be removed in 20 seconds
    time.sleep(20.0)
    for p in ["1.zip", "2.zip", "3.zip"]:
        try:
            os.remove(p)
        except:
            pass


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
