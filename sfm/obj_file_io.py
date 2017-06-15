#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**中文文档**

object file io是一个将Python对象对单个本地文件的I/O



"""

import os
import time
import zlib
import base64
import shutil
import logging
import inspect

# logging util
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


def prt_console(message, verbose):
    """Print message to console, if ``verbose`` is True. 
    """
    if verbose:
        logger.info(message)


# dump, safe_dump, load
def _dump(obj, abspath,
          dumper_func=None,
          compress=True,
          overwrite=False,
          verbose=False,
          **kwargs):
    """Dump object to file.

    :param abspath: The file path you want dump to.
    :type abspath: str

    :param dumper_func: A dumper function that takes an object as input, return
        binary.
    :type dumper_func: callable function

    :param compress: default ``False``. If True, then compress binary.
    :type compress: bool

    :param overwrite: default ``False``, If ``True``, when you dump to 
      existing file, it silently overwrite it. If ``False``, an alert 
      message is shown. Default setting ``False`` is to prevent overwrite 
      file by mistake.
    :type overwrite: boolean

    :param verbose: default True, help-message-display trigger.
    :type verbose: boolean
    """
    if not inspect.isfunction(dumper_func):
        raise TypeError("dumper_func has to be a function take object as input "
                        "and return binary!")

    prt_console("\nDump to '%s' ..." % abspath, verbose)
    if os.path.exists(abspath):
        if not overwrite:
            prt_console(
                "    Stop! File exists and overwrite is not allowed",
                verbose,
            )
            return

    st = time.clock()

    b = dumper_func(obj, **kwargs)
    if compress:
        b = zlib.compress(b)
    with open(abspath, "wb") as f:
        f.write(b)

    elapsed = time.clock() - st
    prt_console("    Complete! Elapse %.6f sec." % elapsed, verbose)

    return b


def _safe_dump(obj, abspath,
               dumper_func=None,
               compress=True,
               verbose=False,
               **kwargs):
    """A stable version of :func:`._dump`, this method silently overwrite 
    existing file.

    There's a issue with :func:`_dump`: If your program is 
    interrupted while writing, you got an incomplete file, and you also 
    lose the original file. So this method write json to a temporary file 
    first, then rename to what you expect, and silently overwrite old one. 
    This way can guarantee atomic write operation.

    **中文文档**

    在对文件进行写入时, 如果程序中断, 则会留下一个不完整的文件。如果使用了
    覆盖式写入, 则我们即没有得到新文件, 同时也丢失了原文件。所以为了保证
    写操作的原子性(要么全部完成, 要么全部都不完成), 更好的方法是: 首先将
    文件写入一个临时文件中, 完成后再讲文件重命名, 覆盖旧文件。这样即使中途
    程序被中断, 也仅仅是留下了一个未完成的临时文件而已, 不会影响原文件。
    """
    abspath_temp = "%s.tmp" % abspath
    b = _dump(
        obj,
        abspath_temp,
        dumper_func=dumper_func,
        compress=compress,
        overwrite=True,
        verbose=verbose,
        **kwargs
    )
    shutil.move(abspath_temp, abspath)

    return b


def _load(abspath,
          loader_func=None,
          decompress=True,
          verbose=False,
          **kwargs):
    """load object from file.

    :param abspath: The file path you want load from.
    :type abspath: str

    :param loader_func: A loader function that takes binary as input, return
        an object.
    :type loader_func: callable function

    :param decompress: default ``False``. If True, then decompress binary.
    :type decompress: bool

    :param verbose: default True, help-message-display trigger.
    :type verbose: boolean
    """
    if not inspect.isfunction(loader_func):
        raise TypeError("loader_func has to be a function take binary as input "
                        "and return an object!")

    prt_console("\nLoad from '%s' ..." % abspath, verbose)
    if not os.path.exists(abspath):
        raise ValueError("'%s' doesn't exist." % abspath)

    st = time.clock()

    with open(abspath, "rb") as f:
        b = f.read()
        if decompress:
            b = zlib.decompress(b)
    obj = loader_func(b, **kwargs)

    elapsed = time.clock() - st
    prt_console("    Complete! Elapse %.6f sec." % elapsed, verbose)

    return obj


if __name__ == "__main__":
    import pickle
    import functools

    def pickle_dumper(obj):
        return pickle.dumps(obj)

    def pickle_loader(b):
        return pickle.loads(b)

    def test_dumper_loader():
        obj = dict(a=1, b=2)
        b = pickle_dumper(obj)
        obj = pickle_loader(b)

    test_dumper_loader()

    def test_partial():
        dump = functools.partial(_dump, dumper_func=pickle_dumper)
        safe_dump = functools.partial(_safe_dump, dumper_func=pickle_dumper)
        load = functools.partial(_load, loader_func=pickle_loader)

        obj = dict(a=1, b=2, c=3)
        b = dump(obj, "data.pk", verbose=True)
        b = safe_dump(obj, "data.pk", verbose=True)
        obj1 = load("data.pk", verbose=True)
        assert obj == obj1

    test_partial()
