# -*- coding: utf-8 -*-

import os
import pytest
from sfm import lines_count


def test_lines_count():
    assert lines_count.count_lines(__file__) >= 22


def test_lines_stats():
    n_files, n_lines = lines_count.lines_stats(
        os.path.dirname(__file__), lines_count.filter_python_script)
    assert n_files >= 17
    assert n_lines >= 1096


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
