# -*- coding: utf-8 -*-

"""
This module provide extensive class and method for the built-in Exception system.
"""

import sys
import traceback
import attr


@attr.s
class Error(object):
    """Advance exception info data container.

    :param exc_value: Exception, the Exception instance.
    :param filename: str, the file name of the error.
    :param line_num: int, the line number of where the error happens.
    :param func_name: str, the closest function who raise the error.
    :param code: str, code line of where the error happens.
    """
    exc_value = attr.ib()
    filename = attr.ib()
    line_num = attr.ib()
    func_name = attr.ib()
    code = attr.ib()

    @property
    def exc_type(self):
        return self.exc_value.__class__

    @property
    def formatted(self):
        template = "`{exc_value.__class__.__name__}: {exc_value}`, appears in `{filename}` at line {line_num} in `{func_name}()`, code: `{code}`"
        return template.format(
            exc_value=self.exc_value,
            filename=self.filename,
            line_num=self.line_num,
            func_name=self.func_name,
            code=self.code,
        )


@attr.s
class ErrorTraceBackChain(object):
    """
    A error trace back chain data container class. Trace error from end point
    back to start point.

    Example usage::

        try:
            some_func(**kwargs)
        except SomeError:
            etbc = ErrorTraceBackChain.get_last_exc_info()
            ... defines how do you want to log relative exceptions
    """
    errors = attr.ib(default=attr.Factory(list))

    @errors.validator
    def check_errors(self, attribute, value):
        if not isinstance(value, list):
            raise TypeError("errors must be list of Error!")

        for error in value:
            if not isinstance(error, Error):
                raise TypeError("errors must be list of Error!")

    @property
    def raised_error(self):
        """
        The error of where it is raised, the end point of the trace back chain.
        """
        # This style tells the interpreter it returns a Error type.
        return Error(**attr.asdict(self.errors[0]))

    @property
    def source_error(self):
        """
        The source of the error, the start point of the track back chain.
        """
        return Error(**attr.asdict(self.errors[-1]))

    @classmethod
    def get_last_exc_info(cls):
        """Get rich info of last raised error.

        :returns: a ErrorTrackBack instance.
        """
        exc_type, exc_value, exc_tb = sys.exc_info()

        errors = list()
        for filename, line_num, func_name, code in traceback.extract_tb(exc_tb):
            error = Error(
                exc_value=exc_value,
                filename=filename,
                line_num=line_num,
                func_name=func_name,
                code=code,
            )
            errors.append(error)
        return cls(errors=errors)

    def __len__(self):
        return len(self.errors)

    def __iter__(self):
        return iter(self.errors)


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
