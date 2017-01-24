#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from collections import OrderedDict
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func, distinct

try:
    import pandas as pd
except:
    pass

try:
    from prettytable import from_db_cursor
except:
    pass


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


def select_column(engine, *columns):
    """Select single column.
    
    :returns headers: headers
    :return data: list of row
    
    **中文文档**
    
    - 在选择单列时, 返回的是 str, list
    - 在选择多列时, 返回的是 str list, list of list
    
    返回单列或多列的数据。
    """
    s = select(columns)
    if len(columns) == 1:
        c_name = columns[0].name
        array = [row[0] for row in engine.execute(s)]
        header, data = c_name, array
        return header, data
    else:
        # from same table
        if len({column.table.name for column in columns}) == 1:
            headers = [column.name for column in columns]
        else:
            headers = [column.__str__() for column in columns]
            
        data = [tuple(row) for row in engine.execute(s)]
        return headers, data


def select_distinct_column(engine, *columns):
    """Select distinct column(columns).

    **中文文档**

    distinct语句的语法糖函数。
    """
    s = select(columns).distinct()
    if len(columns) == 1:
        c_name = columns[0].name
        return [row[c_name] for row in engine.execute(s)]
    else:
        return [[row[column.name] for column in columns] for row in engine.execute(s)]


def sql_to_csv(sql, engine, filepath, chunksize=1000):
    """Export sql result to csv file.

    :param sql: :class:`sqlalchemy.sql.selectable.Select`
    :param engine: :class:'sqlalchemy.engine.base.Engine'
    :param filepath: file path
    :param chunksize: number of rows write to csv each time.

    **中文文档**

    将执行sql的结果中的所有数据, 以生成器的方式(一次只使用一小部分内存), 将
    整个结果写入csv文件。
    """
    columns = [str(column.name) for column in sql.columns]
    with open(filepath, "w") as f:
        # write header
        df = pd.DataFrame([], columns=columns)
        df.to_csv(f, header=True, index=False)

        # iterate big database table
        result_proxy = engine.execute(sql)
        while True:
            data = result_proxy.fetchmany(chunksize)
            if len(data) == 0:
                break
            else:
                df = pd.DataFrame(data, columns=columns)
                df.to_csv(f, header=False, index=False)


def table_to_csv(table, engine, filepath, chunksize=1000):
    """Export entire table to a csv file.

    **中文文档**

    将整个表中的所有数据, 写入csv文件。
    """
    sql = select([table])
    sql_to_csv(sql, engine, filepath, chunksize)
    
    
def sql_to_pretty_table(sql, engine):
    """
    
    **中文文档**
    
    根据sql, 获取pretty table。
    """
    # 注意, from_db_cursor是从原生的数据库游标通过调用fetchall()方法来获取数据。
    # 而sqlalchemy返回的是ResultProxy类。所以我们需要从中获取游标
    # 至于为什么不能直接使用 from_db_cursor(engine.execute(sql).cursor) 的语法
    # 我也不知道为什么
    result_proxy = engine.execute(sql)
    table = from_db_cursor(result_proxy.cursor)
    return table