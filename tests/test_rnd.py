#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sfm.rnd import *


def test_rnd():
    rand_str(32)
    rand_hexstr(12)
    rand_pwd(12)
    rand_phone()
    rand_ssn()
    rand_email()
    rand_article()


if __name__ == "__main__":
    import py
    import os
    py.test.cmdline.main("%s --tb=native -s" % os.path.basename(__file__))