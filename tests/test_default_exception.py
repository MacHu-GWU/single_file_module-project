#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm.default_exception import declare_base


def test_default_exception():
    class DataError(declare_base(erroName=True)):
        default = "This is DEFAULT message"
        
    try:
        raise DataError
    except Exception as e:
        assert str(e) == "DataError: This is DEFAULT message"
         
    try:
        raise DataError("This is CUSTOMIZE message")
    except Exception as e:
        assert str(e) == "DataError: This is CUSTOMIZE message"


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
