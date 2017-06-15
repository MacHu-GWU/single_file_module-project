#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provide extensive class and method for the built-in Exception system.
"""

import sys
import traceback


def get_last_exc_info():
    """Get last raised exception, and format the error message.
    """
    exc_type, exc_value, exc_tb = sys.exc_info()
    for filename, line_num, func_name, code in traceback.extract_tb(exc_tb):
        tmp = "{exc_value.__class__.__name__}: {exc_value}, appears in '{filename}' at line {line_num} in {func_name}(), code: {code}"
        info = tmp.format(
            exc_value=exc_value,
            filename=filename,
            line_num=line_num,
            func_name=func_name,
            code=code,
        )
        return info


class ExceptionHavingDefaultMessage(Exception):
    """A Exception class with default error message.
    """
    default_message = None

    def __str__(self):
        length = len(self.args)
        if length == 0:
            if self.default_message is None:
                raise NotImplementedError("default_message is not defined!")
            else:
                return self.default_message
        elif length == 1:
            return str(self.args[0])
        else:
            return str(self.args)
