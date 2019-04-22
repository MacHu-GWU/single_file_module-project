# -*- coding: utf-8 -*-

"""
This module provides more ``marshmallow.fields.Fields``.
"""

from six import string_types
from marshmallow import fields, ValidationError


class AllowNoneField(fields.Field):
    """This field always allow None.

    **中文文档**

    默认允许None值。
    """

    def __init__(self, *args, **kwargs):
        kwargs["allow_none"] = True
        super(AllowNoneField, self).__init__(*args, **kwargs)


class AutoConvertField(AllowNoneField):
    """This field always call ``self.convert`` method before load and dump.

    **中文文档**

    在load和dump之前都自动调用covert函数进行数据预处理。常用于int, float或
    string这一类原生类。
    """

    def convert(self, value):
        raise NotImplementedError

    def _serialize(self, value, attr, obj):
        return self.convert(value)

    def _deserialize(self, value, attr, data):
        return self.convert(value)


class NonEmptyStringField(AutoConvertField):
    """A non empty string field.

    **中文文档**

    非空字符串。
    """

    def convert(self, value):
        if value is None:
            return None

        if isinstance(value, string_types):
            value = value.strip()
            if value:
                return value
            else:
                return None
        else:
            raise ValidationError("Not a string type.")


class TitleStringField(AutoConvertField):
    """Titlized string.

    **中文文档**

    标题格式的字符串。

    - 字符串
    - 前后都没有空格
    - 不得出现连续两个以上的空格
    - 每个单词首字母大写, 其他字母小写
    """

    def convert(self, value):
        if value is None:
            return None

        if isinstance(value, string_types):
            value = value.strip()
            if value:
                chunks = list()
                for s in [s.strip() for s in value.split(" ") if s.strip()]:
                    if str.isalpha(s):
                        s = s[0].upper() + s[1:].lower()
                        chunks.append(s)
                return " ".join(chunks)
            else:
                return None
        else:
            raise ValidationError("Not a string type")


class LowerStringField(AutoConvertField):
    """Lowercased string.

    **中文文档**

    - 前后没有空格
    - 全部小写
    """

    def convert(self, value):
        if value is None:
            return None

        if isinstance(value, string_types):
            value = value.strip().lower()
            if value:
                return value
            else:
                return None
        else:
            raise ValidationError("Not a string type")


class UpperStringField(AutoConvertField):
    """Uppercased string.

    **中文文档**

    - 前后没有空格
    - 全部小写
    """

    def convert(self, value):
        if value is None:
            return None

        if isinstance(value, string_types):
            value = value.strip().upper()
            if value:
                return value
            else:
                return None
        else:
            raise ValidationError("Not a string type")
