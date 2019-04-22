#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module is to make regular expression easier to use.
With some built-in compiled pattern, we can use human language-like syntax to 
generate re pattern.
"""

import re


def extract_by_prefix_surfix(text,
                             prefix,
                             surfix,
                             minlen=None,
                             maxlen=None,
                             include=False):
    """Extract the text in between a prefix and surfix. It use non-greedy match.

    :param text: text body
    :type text: str

    :param prefix: the prefix
    :type prefix: str

    :param surfix: the surfix
    :type surfix: str

    :param minlen: the min matched string length
    :type minlen: int

    :param maxlen: the max matched string length
    :type maxlen: int

    :param include: whether if include prefix and surfix
    :type include: bool
    """
    if minlen is None:
        minlen = 0
    if maxlen is None:
        maxlen = 2 ** 30
    pattern = r"""(?<=%s)[\s\S]{%s,%s}?(?=%s)""" % (
        prefix, minlen, maxlen, surfix)
    if include:
        return [prefix + s + surfix for s in re.findall(pattern, text)]
    else:
        return re.findall(pattern, text)


def extract_number(text):
    """Extract digit character from text.
    """
    result = list()
    chunk = list()
    valid_char = set(".1234567890")
    for char in text:
        if char in valid_char:
            chunk.append(char)
        else:
            result.append("".join(chunk))
            chunk = list()
    result.append("".join(chunk))

    result_new = list()
    for number in result:
        if "." in number:
            try:
                result_new.append(float(number))
            except:
                pass
        else:
            try:
                result_new.append(int(number))
            except:
                pass

    return result_new


_regex_extract_email = re.compile(
    r"""([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)""")
_regex_validate_email = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def extract_email(text):
    """Extract email from text.
    """
    result = list()
    for tp in re.findall(_regex_extract_email, text.lower()):
        for email in tp:
            if re.match(_regex_validate_email, email):
                result.append(email)
    return result


_regex_url = re.compile(
    r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""")

_regex_web_url = re.compile(
    r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""")
"""ref: https://github.com/rcompton/ryancompton.net/blob/master/assets/praw_drugs/urlmarker.py
"""


def extract_web_url(text):
    """Extract url from text.
    """
    return re.findall(_regex_web_url, text)


_regex_date_iso = "\d{4}-\d{1,2}-\d{1,2}"


def extract_date_iso(text):
    """Extract iso date format (%yyyy-%mm-%dd) from text.
    """
    return re.findall(_regex_date_iso, text)


_regex_date_us = "\d{1,2}/\d{1,2}/\d{2,4}"


def extract_date_us(text):
    """Extract US format (%m/%d/%y) from text
    """
    return re.findall(_regex_date_us, text)
