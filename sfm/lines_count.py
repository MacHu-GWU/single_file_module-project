# -*- coding: utf-8 -*-

from pathlib_mate import Path


def filter_python_script(path):
    if path.ext == ".py":
        return True
    else:
        return False


def filter_pure_text(path):
    ext = [".txt", ".rst", ".md"]
    if path.ext in ext:
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
    """Lines count of selected files under a directory.

    :return n_files: number of files
    :return n_lines: number of lines
    """
    n_files = 0
    n_lines = 0
    for p in Path(dir_path).select_file(file_filter):
        n_files += 1
        n_lines += count_lines(p.abspath)
    return n_files, n_lines
