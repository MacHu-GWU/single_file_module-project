#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

**中文文档**

matplotmate提供了一套函数式的命令, 用于时间序列数据的简单绘图。适画用于在R&D中
用于快速观测的图。自定义程度较低, 但是默认设置非常适合研究。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, WeekdayLocator, DayLocator
from matplotlib.dates import HourLocator, MinuteLocator
from matplotlib.dates import DateFormatter
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from itertools import cycle

cycol = cycle("brgcmyk")


def one_day_formatter():
    hours = HourLocator(range(24))
    hoursFmt = DateFormatter("%H:%M")
    minutes = MinuteLocator([30, ])
    minutesFmt = DateFormatter("%M")
    return hours, hoursFmt, minutes, minutesFmt


def one_week_formatter():
    days = DayLocator(range(365))
    daysFmt = DateFormatter("%m-%d")
    hours = HourLocator([3, 6, 9, 12, 15, 18, 21])
    hoursFmt = DateFormatter("%H")
    return days, daysFmt, hours, hoursFmt


def one_month_formatter():
    days = DayLocator(range(365))
    daysFmt = DateFormatter("%m-%d")
    return days, daysFmt, None, None


def one_quarter_formatter():
    months = MonthLocator(range(1, 13))
    monthsFmt = DateFormatter("%Y-%m")
    days = DayLocator([7, 14, 21, 28])
    daysFmt = DateFormatter("%dth")
    return months, monthsFmt, days, daysFmt


def one_year_formatter():
    months = MonthLocator(range(1, 13))
    monthsFmt = DateFormatter("%Y-%m")
    days = DayLocator([15])
    daysFmt = DateFormatter("%d")
    return months, monthsFmt, days, daysFmt


def format_x_tick(axis,
                  major_locator=None,
                  major_formatter=None,
                  minor_locator=None,
                  minor_formatter=None):
    """

    **中文文档**

    设置X轴格式。
    """
    if major_locator:
        axis.xaxis.set_major_locator(major_locator)
    if major_formatter:
        axis.xaxis.set_major_formatter(major_formatter)
    if minor_locator:
        axis.xaxis.set_minor_locator(minor_locator)
    if minor_formatter:
        axis.xaxis.set_minor_formatter(minor_formatter)

    axis.autoscale_view()
    plt.setp(axis.xaxis.get_majorticklabels(), rotation=90)
    plt.setp(axis.xaxis.get_minorticklabels(), rotation=90)
    axis.grid()


def set_title_xlabel_ylabel(axis, title, xlabel, ylabel):
    """

    **中文文档**

    设置标题, x坐标和y坐标的单位标签。
    """
    if title:
        axis.set_title(title)

    if xlabel:
        axis.set_xlabel(xlabel)
    else:
        axis.set_xlabel("Time")

    if ylabel:
        axis.set_ylabel(ylabel)
    else:
        axis.set_ylabel("Value")


def set_ylim(axis, y):
    """set min and max value of y axis

    :param y: multiple y axis tuple.

    **中文文档**

    设置y坐标的最大最小值。
    """
    y_min, y_max = get_yAxis_limit(np.array(y).flatten())
    axis.set_ylim([y_min, y_max])


def set_legend(axis, lines, legend):
    """Set line legend.

    **中文文档**

    设置图例。
    """
    try:
        if legend:
            axis.legend(lines, legend)
    except Exception as e:
        raise ValueError("invalid 'legend', Error: %s" % e)


def get_max(array):
    """Get maximum value.

    **中文文档**

    获得最大值。
    """
    largest = -np.inf
    for i in array:
        try:
            if i > largest:
                largest = i
        except:
            pass
    if np.isinf(largest):
        raise ValueError("there's no numeric value in array!")
    else:
        return largest


def get_min(array):
    """Get minimum value.

    **中文文档**

    获得最小值。
    """
    smallest = np.inf
    for i in array:
        try:
            if i < smallest:
                smallest = i
        except:
            pass
    if np.isinf(smallest):
        raise ValueError("there's no numeric value in array!")
    else:
        return smallest


def get_yAxis_limit(y, lower=0.05, upper=0.2):
    """

    **中文文档**

    计算y坐标轴的最小和最大坐标。
    """
    smallest = get_min(y)
    largest = get_max(y)
    gap = largest - smallest
    y_min = smallest - lower * gap
    y_max = largest + upper * gap
    return y_min, y_max


def create_figure():
    figure = plt.figure(figsize=(20, 10))
    axis = figure.add_subplot(1, 1, 1)
    return figure, axis


def preprocess_x_y(x, y):
    """Preprocess x, y input data.

    **中文文档**

    预处理输入的x, y数据。
    """
    if not isinstance(x, (tuple, list)):
        return (x,), (y,)
    else:
        return x, y


def plot_time_series(x, y,
                     xlabel=None, ylabel=None,
                     x_major_locattor=None, x_major_formatter=None,
                     x_minor_locattor=None, x_minor_formatter=None,
                     title=None, legend=None):
    """
    :param x: time array or tuple
    :param y: time array or tuple

    **中文文档**

    为时间序列数据画图。
    """
    x, y = preprocess_x_y(x, y)

    plt.close("all")
    figure, axis = create_figure()

    lines = list()
    for time, value in zip(x, y):
        lines.append(axis.plot(time, value)[0])

    format_x_tick(axis,
                  x_major_locattor, x_major_formatter,
                  x_minor_locattor, x_minor_formatter,)
    set_ylim(axis, y)
    set_title_xlabel_ylabel(axis, title, xlabel, ylabel)
    set_legend(axis, lines, legend)
    return plt


def plot_one_day(x, y, xlabel=None, ylabel=None, title=None, legend=None):
    """
    """
    (
        x_major_locattor,
        x_major_formatter,
        x_minor_locattor,
        x_minor_formatter,
    ) = one_day_formatter()
    return plot_time_series(x, y, xlabel, ylabel,
                            x_major_locattor, x_major_formatter,
                            x_minor_locattor, x_minor_formatter,
                            title, legend,
                            )


def plot_one_week(x, y, xlabel=None, ylabel=None, title=None, legend=None):
    """
    """
    (
        x_major_locattor,
        x_major_formatter,
        x_minor_locattor,
        x_minor_formatter,
    ) = one_week_formatter()
    return plot_time_series(x, y, xlabel, ylabel,
                            x_major_locattor, x_major_formatter,
                            x_minor_locattor, x_minor_formatter,
                            title, legend,
                            )


def plot_one_month(x, y, xlabel=None, ylabel=None, title=None, legend=None):
    """
    """
    (
        x_major_locattor,
        x_major_formatter,
        x_minor_locattor,
        x_minor_formatter,
    ) = one_month_formatter()
    return plot_time_series(x, y, xlabel, ylabel,
                            x_major_locattor, x_major_formatter,
                            x_minor_locattor, x_minor_formatter,
                            title, legend,
                            )


def plot_one_quarter(x, y, xlabel=None, ylabel=None, title=None, legend=None):
    """
    """
    (
        x_major_locattor,
        x_major_formatter,
        x_minor_locattor,
        x_minor_formatter,
    ) = one_quarter_formatter()
    return plot_time_series(x, y, xlabel, ylabel,
                            x_major_locattor, x_major_formatter,
                            x_minor_locattor, x_minor_formatter,
                            title, legend,
                            )


def plot_one_year(x, y, xlabel=None, ylabel=None, title=None, legend=None):
    """
    """
    (
        x_major_locattor,
        x_major_formatter,
        x_minor_locattor,
        x_minor_formatter,
    ) = one_year_formatter()
    return plot_time_series(x, y, xlabel, ylabel,
                            x_major_locattor, x_major_formatter,
                            x_minor_locattor, x_minor_formatter,
                            title, legend,
                            )

#--- Twin Axis ---


def plot_two_scales(x1, y1, x2, y2, xlabel=None, ylabel1=None, ylabel2=None,
                    x_major_locattor=None, x_major_formatter=None,
                    x_minor_locattor=None, x_minor_formatter=None,
                    title=None, legend=None):
    """
    
    **中文文档**
    
    将两种不同尺度的线画在一张图上。
    """
    x1, y1 = preprocess_x_y(x1, y1)
    x2, y2 = preprocess_x_y(x2, y2)

    plt.close("all")
    figure, axis1 = create_figure()
    axis2 = axis1.twinx()

    lines = list()
    for time, value in zip(x1, y1):
        lines.append(axis1.plot(time, value, c=next(cycol))[0])

    for time, value in zip(x2, y2):
        lines.append(axis2.plot(time, value, c=next(cycol))[0])

    format_x_tick(axis1,
                  x_major_locattor, x_major_formatter,
                  x_minor_locattor, x_minor_formatter,)
    set_ylim(axis1, y1)
    set_ylim(axis2, y2)
    set_title_xlabel_ylabel(axis1, title, xlabel, ylabel1)
    set_title_xlabel_ylabel(axis2, title, xlabel, ylabel2)
    set_legend(axis1, lines, legend)
    return plt

#--- Unittest ---
if __name__ == "__main__":
    import pytest
    from rolex import rolex

    def test_get_max():
        assert get_max(np.array([0, 1, 2])) == 2
        assert get_max(np.array([None, 1, 2])) == 2
        with pytest.raises(ValueError):
            get_max(np.array([None, None, None]))

    test_get_max()

    def test_plot_one_day():
        x = rolex.time_series(
            "2016-01-01 00:00:00", "2016-01-01 23:59:59", freq="10min")
        y1 = np.random.random(len(x))
        y2 = np.random.random(len(x))
        plot_one_day((x, x), (y1, y2),
                     xlabel="Time", ylabel="Stock Value", title="Stock Trends",
                     legend=["Stock 1", "Stock 2"]).show()

    test_plot_one_day()

    def test_plot_one_week():
        x = rolex.time_series(
            "2016-01-01 00:00:00", "2016-01-07 23:59:59", freq="3hour")
        y1 = np.random.random(len(x))
        y2 = np.random.random(len(x))
        plot_one_week((x, x), (y1, y2),
                      xlabel="Time", ylabel="Stock Value", title="Stock Trends",
                      legend=["Stock 1", "Stock 2"]).show()

    # test_plot_one_week()

    def test_plot_one_month():
        x = rolex.time_series(
            "2016-01-01 00:00:00", "2016-01-31 23:59:59", freq="12hour")
        y1 = np.random.random(len(x))
        y2 = np.random.random(len(x))
        plot_one_month((x, x), (y1, y2),
                       xlabel="Time", ylabel="Stock Value", title="Stock Trends",
                       legend=["Stock 1", "Stock 2"]).show()

    # test_plot_one_month()

    def test_plot_one_quarter():
        x = rolex.time_series(
            "2016-01-01 00:00:00", "2016-03-31 23:59:59", freq="1day")
        y1 = np.random.random(len(x))
        y2 = np.random.random(len(x))
        plot_one_quarter((x, x), (y1, y2),
                         xlabel="Time", ylabel="Stock Value", title="Stock Trends",
                         legend=["Stock 1", "Stock 2"]).show()

    # test_plot_one_quarter()

    def test_plot_one_year():
        x = rolex.time_series(
            "2016-01-01 00:00:00", "2016-12-31 23:59:59", freq="7day")
        y1 = np.random.random(len(x))
        y2 = np.random.random(len(x))
        plot_one_year((x, x), (y1, y2),
                      xlabel="Time", ylabel="Stock Value", title="Stock Trends",
                      legend=["Stock 1", "Stock 2"]).show()

    # test_plot_one_year()

    def test_plot_two_scales():
        x = rolex.time_series(
            "2016-01-01 00:00:00", "2016-01-01 23:59:59", freq="10min")
        y1 = np.random.random(len(x))
        y2 = np.random.random(len(x)) * 10
        plot_two_scales(x, y1, x, y2,
                        xlabel="Time", ylabel1="Interests Value", ylabel2="Stock Value", title="Stock Trends",
                        legend=["Interests", "Stock"]).show()

#     test_plot_two_scales()
