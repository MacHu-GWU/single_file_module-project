#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib_mate import Path

dirpath_list = [
    "sfm",
    "tests",
]
for dirpath in dirpath_list:
    p = Path(dirpath)
    p.autopep8()