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
    return zip( *(l for col, l in df.iteritems()) )


class IOTool(object):
    """Input/Output utility methods.
    
    """
    @staticmethod
    def csv_tuple_iterator(path, chunksize, **kwargs):
        """
        
        :yield tuple: 
        
        **中文文档**
        
        对dataframe进行tuple风格的高性能行遍历。
        
        对用pandas从csv文件读取的dataframe进行逐行遍历时, iterrows和itertuple
        都不是性能最高的方法。这是因为iterrows要生成Series对象, 而itertuple
        也要对index进行访问。所以本方法是使用内建zip方法对所有的column进行打包
        解压, 所以性能上是最佳的。
        """
        for df in pd.read_csv(path, iterator=True, chunksize=chunksize, **kwargs):
            for tp in itertuple(df):
                yield tp
                

class Transform(object):
    """Data transform utility methods.
    
    
    """
    @staticmethod
    def key_row_table(df, index_col=None, use_ordered_dict=True):
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
