#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from sfm.rnd import *

def test_rnd():
    rand_str(32)
    rand_hexstr(12)
    rand_alphastr(12)
    rand_pwd(12)
    rand_phone()
    rand_ssn()
    rand_email()
    rand_article()
    
    first_name()
    last_name()
    name()
    address()
    company()


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])