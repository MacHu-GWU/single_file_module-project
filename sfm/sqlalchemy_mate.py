#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func, distinct


def grouper_list(l, n):
    """Evenly divide list into fixed-length piece, no filled value if chunk
    size smaller than fixed-length.

    Example::

        >>> list(grouper(range(10), n=3)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    **中文文档**

    将一个列表按照尺寸n, 依次打包输出, 有多少输出多少, 并不强制填充包的大小到n。

    下列实现是按照性能从高到低进行排列的:

    - 方法1: 建立一个counter, 在向chunk中添加元素时, 同时将counter与n比较, 如果一致
      则yield。然后在最后将剩余的item视情况yield。
    - 方法2: 建立一个list, 每次添加一个元素, 并检查size。
    - 方法3: 调用grouper()函数, 然后对里面的None元素进行清理。
    """
    chunk = list()
    counter = 0
    for item in l:
        counter += 1
        chunk.append(item)
        if counter == n:
            yield chunk
            chunk = list()
            counter = 0
    if len(chunk) > 0:
        yield chunk


def smart_insert(engine, table, data, minimal_size=5):
    """An optimized Insert strategy.

    **中文文档**

    在Insert中, 如果已经预知不会出现IntegrityError, 那么使用Bulk Insert的速度要
    远远快于逐条Insert。而如果无法预知, 那么我们采用如下策略:

    1. 尝试Bulk Insert, Bulk Insert由于在结束前不Commit, 所以速度很快。
    2. 如果失败了, 那么对数据的条数开平方根, 进行分包, 然后对每个包重复该逻辑。
    3. 若还是尝试失败, 则继续分包, 当分包的大小小于一定数量时, 则使用逐条插入。
      直到成功为止。

    该Insert策略在内存上需要额外的 sqrt(nbytes) 的开销, 跟原数据相比体积很小。
    但时间上是各种情况下平均最优的。
    """
    insert = table.insert()

    if isinstance(data, list):
        # 首先进行尝试bulk insert
        try:
            engine.execute(insert, data)
        # 失败了
        except IntegrityError:
            # 分析数据量
            n = len(data)
            # 如果数据条数多于一定数量
            if n >= minimal_size ** 2:
                # 则进行分包
                n_chunk = math.floor(math.sqrt(n))
                for chunk in grouper_list(data, n_chunk):
                    smart_insert(engine, table, chunk, minimal_size)
            # 否则则一条条地逐条插入
            else:
                for row in data:
                    try:
                        engine.execute(insert, row)
                    except IntegrityError:
                        pass
    else:
        try:
            engine.execute(insert, data)
        except IntegrityError:
            pass


def count_row(engine, table):
    """Return number of rows in a table.
    
    **中文文档**
    
    返回一个表中的行数。
    """
    return engine.execute(table.count()).fetchone()[0]


def select_all(engine, table):
    """Select everything from a table.
    
    **中文文档**
    
    选取所有数据。
    """
    s = select([table])
    return engine.execute(s)


def select_column(engine, column):
    """Select single column.
    
    **中文文档**
    
    返回单列的数据。
    """
    s = select([column])
    return [row[column.name] for row in engine.execute(s)]


def select_distinct_column(engine, *columns):
    """Select distinct column(columns).
    
    **中文文档**
    
    distinct语句的语法糖函数。
    """
    s = select(columns).distinct()
    if len(columns) == 1:
        return [row[columns[0].name] for row in engine.execute(s)]
    else:
        return [[row[column.name] for column in columns] for row in engine.execute(s)]