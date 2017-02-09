#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zlib
import base64


def encode_base64_urlsafe(text):
    """Convert any utf-8 string to url safe string using base64 encoding.
    
    **中文文档**
    
    将任意utf-8字符串用base64编码算法编码为纯数字和字母。
    """
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("utf-8")


def decode_base64_urlsafe(text):
    """Reverse operation of :func:`encode_base64_urlsafe`.
    
    **中文文档**
    
    将base64字符串解码为原字符串。
    """
    return base64.urlsafe_b64decode(text.encode("utf-8")).decode("utf-8")


#--- compress/decompress ---
def compress_str(s):
    """use zip and base64 encoding to compress arbitrary utf-8 string to a 
    shorter utf-8 string. 
    
    Procedure:
    
    1. str -> utf-8 bytes
    2. utf-8 bytes --- zip compress ---> bytes
    3. bytes -> urlsafe_b64encode bytes
    4. urlsafe_b64encode bytes -> str
    
    **中文文档**
    
    将字符串压缩成另一个字符串
    """
    return base64.urlsafe_b64encode(zlib.compress(s.encode("utf-8"))).decode("utf-8")


def decompress_str(s):
    """opposite of :func:`compress_str`.
    
    Procedure:
    
    1. str -> utf-8 bytes
    2. utf-8 bytes -> b64 decode bytes
    3. urlsafe_b64decode bytes --- zip decompress ---> bytes
    4. bytes -> str
    
    **中文文档**
    
    将字符串解压缩为另一个字符串
    """
    return zlib.decompress(base64.urlsafe_b64decode(s.encode("utf-8"))).decode("utf-8")