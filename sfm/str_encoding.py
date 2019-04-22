# -*- coding: utf-8 -*-

import base64
import binascii


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


def encode_hexstr(text):
    """Convert any utf-8 string to hex string.

    **中文文档**

    将任意utf-8字符串编码为16进制字符串。
    """
    return binascii.b2a_hex(text.encode("utf-8")).decode("utf-8")


def decode_hexstr(text):
    """Reverse operation of :func:`encode_hexstr`.

    **中文文档**

    将16进制字符串解码为原字符串。
    """
    return binascii.a2b_hex(text.encode("utf-8")).decode("utf-8")
