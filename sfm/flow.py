# -*- coding: utf-8 -*-


"""
function logic flow constructor.
"""


def try_ntime(max_try, func, *args, **kwargs):
    """
    Try execute a function n times, until no exception raised or tried
    ``max_try`` times.

    **中文文档**

    反复尝试执行一个函数若干次。直到成功为止或是重复尝试 ``max_try`` 次。期间
    只要有一次成功, 就正常返回。如果一次都没有成功, 则行为跟最后一次执行了
    ``func(*args, **kwargs)`` 一样。
    """
    if max_try < 1:
        raise ValueError

    for i in range(max_try):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e

    raise last_exception

