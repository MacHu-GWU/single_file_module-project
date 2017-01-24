#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] == 2:
    from itertools import (
        izip as zip,
    )
from collections import OrderedDict
import pandas as pd


def itertuple(df):
    """High performance tuple style iterator.

    **中文文档**

    对dataframe进行tuple风格的高性能行遍历。
    """
    return zip(*(l for col, l in df.iteritems()))


class IOTool(object):

    """Input/Output utility methods.

    """
    @staticmethod
    def iterate_tuple_from_csv(path,
                               iterator=False,
                               chunksize=None,
                               skiprows=None,
                               nrows=None,
                               **kwargs):
        """

        :yield tuple: 

        **中文文档**

        对dataframe进行tuple风格的高性能行遍历。

        对用pandas从csv文件读取的dataframe进行逐行遍历时, iterrows和itertuple
        都不是性能最高的方法。这是因为iterrows要生成Series对象, 而itertuple
        也要对index进行访问。所以本方法是使用内建zip方法对所有的column进行打包
        解压, 所以性能上是最佳的。
        """
        kwargs["iterator"] = iterator
        kwargs["chunksize"] = chunksize
        kwargs["skiprows"] = skiprows
        kwargs["nrows"] = nrows

        if iterator is True:
            for df in pd.read_csv(path, **kwargs):
                for tp in itertuple(df):
                    yield tp
        else:
            df = pd.read_csv(path, **kwargs)
            for tp in itertuple(df):
                yield tp
    
    @staticmethod
    def index_row_map_from_csv(path,
                               index_col=None,
                               iterator=False,
                               chunksize=None,
                               skiprows=None,
                               nrows=None,
                               use_ordered_dict=True,
                               **kwargs):
        """
        
        **中文文档**
        
        读取csv, 选择一值完全不重复, 可作为index的列作为index, 生成一个字典
        数据结构, 使得可以通过index直接访问row。
        """
        _kwargs = dict(list(kwargs.items()))
        _kwargs["iterator"] = None
        _kwargs["chunksize"] = None
        _kwargs["skiprows"] = 0
        _kwargs["nrows"] = 1

        df = pd.read_csv(path, index_col=index_col, **_kwargs)
        columns = df.columns

        if index_col is None:
            raise Exception("please give index_col!")

        if use_ordered_dict:
            table = OrderedDict()
        else:
            table = dict()

        kwargs["iterator"] = iterator
        kwargs["chunksize"] = chunksize
        kwargs["skiprows"] = skiprows
        kwargs["nrows"] = nrows

        if iterator is True:
            for df in pd.read_csv(path, index_col=index_col, **kwargs):
                for ind, tp in zip(df.index, itertuple(df)):
                    table[ind] = dict(zip(columns, tp))
        else:
            df = pd.read_csv(path, index_col=index_col, **kwargs)
            for ind, tp in zip(df.index, itertuple(df)):
                table[ind] = dict(zip(columns, tp))

        return table


class Transform(object):

    """Data transform utility methods.


    """
    @staticmethod
    def index_row_map(df, index_col=None, use_ordered_dict=True):
        """

        **中文文档**

        将dataframe以指定列为key, 转化成以行为视角的dict结构, 提升按行index访问
        的速度。若无指定列, 则使用index。
        """
        if index_col:
            index_list = df[index_col]
        else:
            index_list = df.index

        columns = df.columns

        if use_ordered_dict:
            table = OrderedDict()
        else:
            table = dict()

        for ind, tp in zip(index_list, itertuple(df)):
            table[ind] = dict(zip(columns, tp))

        return table
