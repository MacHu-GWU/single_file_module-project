#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from filetool.files import FileCollection


def filter_python_script(winfile):
    if winfile.ext == ".py":
        return True
    else:
        return False


def filter_pure_text(winfile):
    ext = [".txt", ".rst", ".md"]
    if winfile.ext in ext:
        return True
    else:
        return False


def count_lines(abspath):
    """Count how many lines in a pure text file.
    """
    with open(abspath, "rb") as f:
        i = 0
        for line in f:
            i += 1
            pass
        return i


def lines_stats(dir_path, file_filter):
    n_files = 0
    n_lines = 0
    for abspath in FileCollection.from_path_by_criterion(dir_path, file_filter):
        n_files += 1
        n_lines += count_lines(abspath)
    print("files: %s, lines: %s" % (n_files, n_lines))


if __name__ == "__main__":
    import os
    lines_stats(os.path.dirname(__file__), filter_python_script)
