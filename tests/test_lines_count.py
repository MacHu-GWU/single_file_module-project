#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm import lines_count


def test_lines_count():
    assert lines_count.count_lines(__file__) == 14


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])