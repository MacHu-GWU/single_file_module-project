# -*- coding: utf-8 -*-

"""
object file io is a Python object to single file I/O framework. The word
'framework' means you can use any serialization/deserialization algorithm here.

- dump: dump python object to a file.
- safe_dump: add atomic writing guarantee for ``dump``.
- load: load python object from a file.

Features:

1. ``compress``: built-in compress/decompress options.
2. ``overwrite``: an option to prevent from overwrite existing file.
3. ``verbose``: optional built-in logger can display help infomation.

Usage:

suppose you have a function (dumper function, has to take python object as
input, and return a binary object) can dump python object to binary::

    import pickle

    def dump(obj):
        return pickle.dumps(obj)

    def load(binary):
        return pickle.loads(binary)

You just need to add a decorator, and new function will do all magic for you:

    from obj_file_io import dump_func, safe_dump_func, load_func

    @dump_func
    def dump(obj):
        return pickle.dumps(obj)

    @safe_dump_func
    def safe_dump(obj):
        return pickle.dumps(obj)

    @load_func
    def load(binary):
        return pickle.loads(binary)


**中文文档**

object file io是一个将Python对象对单个本地文件的I/O
"""

import os
import time
import zlib
import logging
import inspect
from atomicwrites import atomic_write

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


def _check_serializer_type(serializer_type):
    if serializer_type not in ["binary", "str"]:
        raise ValueError("serializer_type has to be one of 'binary' or 'str'!")


# dump, load
def _dump(obj, abspath, serializer_type,
          dumper_func=None,
          compress=True,
          overwrite=False,
          verbose=False,
          **kwargs):
    """Dump object to file.

    :param abspath: The file path you want dump to.
    :type abspath: str

    :param serializer_type: 'binary' or 'str'.
    :type serializer_type: str

    :param dumper_func: A dumper function that takes an object as input, return
        binary or string.
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
    _check_serializer_type(serializer_type)

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

    b_or_str = dumper_func(obj, **kwargs)
    if serializer_type is "str":
        b = b_or_str.encode("utf-8")
    else:
        b = b_or_str

    if compress:
        b = zlib.compress(b)

    with atomic_write(abspath, overwrite=overwrite, mode="wb") as f:
        f.write(b)

    elapsed = time.clock() - st
    prt_console("    Complete! Elapse %.6f sec." % elapsed, verbose)

    if serializer_type is "str":
        return b_or_str
    else:
        return b


def _load(abspath, serializer_type,
          loader_func=None,
          decompress=True,
          verbose=False,
          **kwargs):
    """load object from file.

    :param abspath: The file path you want load from.
    :type abspath: str

    :param serializer_type: 'binary' or 'str'.
    :type serializer_type: str

    :param loader_func: A loader function that takes binary as input, return
        an object.
    :type loader_func: callable function

    :param decompress: default ``False``. If True, then decompress binary.
    :type decompress: bool

    :param verbose: default True, help-message-display trigger.
    :type verbose: boolean
    """
    _check_serializer_type(serializer_type)

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

    if serializer_type is "str":
        obj = loader_func(b.decode("utf-8"), **kwargs)
    else:
        obj = loader_func(b, **kwargs)

    elapsed = time.clock() - st
    prt_console("    Complete! Elapse %.6f sec." % elapsed, verbose)

    return obj


def dump_func(serializer_type):
    """A decorator for ``_dump(dumper_func=dumper_func, **kwargs)``
    """

    def outer_wrapper(dumper_func):
        def wrapper(*args, **kwargs):
            return _dump(
                *args,
                dumper_func=dumper_func, serializer_type=serializer_type,
                **kwargs
            )

        return wrapper

    return outer_wrapper


def load_func(serializer_type):
    """A decorator for ``_load(loader_func=loader_func, **kwargs)``
    """

    def outer_wrapper(loader_func):
        def wrapper(*args, **kwargs):
            return _load(
                *args,
                loader_func=loader_func, serializer_type=serializer_type,
                **kwargs
            )

        return wrapper

    return outer_wrapper
