#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] == 2:
    from itertools import (
        izip as zip,
    )

import math
import json
from datetime import datetime
from collections import OrderedDict

import pandas as pd
from rolex import rolex


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
        """Read the csv into a dictionary. The key is it's index, the value
        is the dictionary form of the row.

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

    @staticmethod
    def to_sql_smart_insert(df, table, engine, minimal_size=5):
        """An optimized Insert strategy.

        **中文文档**

        一种优化的将大型DataFrame中的数据, 在有IntegrityError的情况下将所有
        好数据存入数据库的方法。
        """
        from sqlalchemy.exc import IntegrityError

        insert = table.insert()

        # 首先进行尝试bulk insert
        try:
            df.to_sql(table.name, engine, index=False, if_exists="append")
        # 失败了
        except IntegrityError:
            # 分析数据量
            n = df.shape[0]
            # 如果数据条数多于一定数量
            if n >= minimal_size ** 2:
                # 则进行分包
                n_chunk = math.floor(math.sqrt(n))
                for sub_df in Transform.grouper_df(df, n_chunk):
                    IOTool.to_sql_smart_insert(
                        sub_df, table, engine, minimal_size)
            # 否则则一条条地逐条插入
            else:
                for sub_df in Transform.grouper_df(df, 1):
                    try:
                        sub_df.to_sql(
                            table.name, engine, index=False, if_exists="append")
                    except IntegrityError:
                        pass


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

    @staticmethod
    def grouper_df(df, n):
        """Evenly divide pd.DataFrame into n rows piece, no filled value 
        if sub dataframe's size smaller than n.
        """
        data = list()
        counter = 0
        for tp in zip(*(l for col, l in df.iteritems())):
            counter += 1
            data.append(tp)
            if counter == n:
                new_df = pd.DataFrame(data, columns=df.columns)
                yield new_df
                data = list()
                counter = 0

        if len(data) > 0:
            new_df = pd.DataFrame(data, columns=df.columns)
            yield new_df

    @staticmethod
    def generic_python_dict_list(df, int_col=None):
        data = json.loads(df.to_json(orient="records", date_format="iso"))

        datetime_col = list()
        for col, dtype in dict(df.dtypes).items():
            if "datetime64" in str(dtype):
                datetime_col.append(col)
        if len(datetime_col) == 0:
            datetime_col = None

        if (int_col is not None) and (not isinstance(int_col, (list, tuple))):
            int_col = [int_col, ]

        if int_col is None and datetime_col is None:
            return data

        elif int_col is None and datetime_col is not None:
            def func(doc):
                for col in datetime_col:
                    try:
                        doc[col] = rolex.str2datetime(doc[col])
                    except:
                        pass
                return doc

        elif int_col is not None and datetime_col is None:
            def func(doc):
                for col in int_col:
                    try:
                        doc[col] = int(doc[col])
                    except:
                        pass
                return doc

        else:
            def func(doc):
                for col in int_col:
                    try:
                        doc[col] = int(doc[col])
                    except:
                        pass

                for col in datetime_col:
                    try:
                        doc[col] = rolex.str2datetime(doc[col])
                    except:
                        pass

                return doc

        return list(map(func, data))
