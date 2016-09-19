#!/usr/bin/env python
# -*- coding: utf-8 -*-

from six import string_types
from marshmallow import fields, ValidationError


class AllowNoneField(fields.Field):
    """
    
    **中文文档**
    
    默认允许None值。
    """
    def __init__(self, *args, **kwargs):
        kwargs["allow_none"] = True
        super(AllowNoneField, self).__init__(*args, **kwargs)


class NonEmptyStringField(AllowNoneField):
    """
    
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
             
    def _serialize(self, value, attr, obj):
        return self.convert(value)
    
    def _deserialize(self, value, attr, data):
        return self.convert(value)


class TitleStringField(AllowNoneField):
    """
    
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
             
    def _serialize(self, value, attr, obj):
        return self.convert(value)
    
    def _deserialize(self, value, attr, data):
        return self.convert(value)