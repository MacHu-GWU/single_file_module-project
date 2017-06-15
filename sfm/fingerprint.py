#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module is built on Python standard hashlib, provides utility method  
to find hash value for a bytes, a string, a Python object or a file.

**中文文档**

本模块提供了一些计算Hash值的简便方法。对于 of_pyobj()方法来说, 请注意在读写时
均使用相同的Python大版本(2/3)。
"""

import os
import sys
import pickle
import hashlib

is_py2 = (sys.version_info[0] == 2)
if is_py2:
    pk_protocol = 2
else:
    pk_protocol = 3


class FingerPrint(object):

    """A hashlib wrapper class allow you to use one line to do hash as you wish.

    Usage::

        >>> from weatherlab.lib.hashes.fingerprint import fingerprint
        >>> print(fingerprint.of_bytes(bytes(123)))
        b1fec41621e338896e2d26f232a6b006

        >>> print(fingerprint.of_text("message"))
        78e731027d8fd50ed642340b7c9a63b3

        >>> print(fingerprint.of_pyobj({"key": "value"}))
        4c502ab399c89c8758a2d8c37be98f69

        >>> print(fingerprint.of_file("fingerprint.py"))
        4cddcb5562cbff652b0e4c8a0300337a
    """
    _mapper = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }

    def __init__(self, algorithm="md5", pk_protocol=pk_protocol):
        self.use(algorithm)
        self.set_return_str()
        self.set_pickle_protocol(pk_protocol)

    def digest_to_int(self, digest):
        """Convert hexdigest str to int.
        """
        return int(digest, 16)

    def use(self, algorithm):
        """Change the hash algorithm you gonna use.
        """
        try:
            self.hash_algo = self._mapper[algorithm.strip().lower()]
        except IndexError:
            template = "'%s' is not supported, try one of %s."
            raise ValueError(template % (algorithm, list(self._mapper)))

    def set_return_int(self):
        """Set to return hex integer.
        """
        self.return_int = True

    def set_return_str(self):
        """Set to return hex string.
        """
        self.return_int = False

    def set_pickle_protocol(self, pk_protocol):
        """Set pickle protocol.
        """
        if pk_protocol not in [2, 3]:
            raise ValueError("pickle protocol has to be 2 or 3!")
        self.pk_protocol = pk_protocol

    def of_bytes(self, py_bytes):
        """Use default hash method to return hash value of bytes.
        """
        m = self.hash_algo()
        m.update(py_bytes)
        if self.return_int:
            return int(m.hexdigest(), 16)
        else:
            return m.hexdigest()

    def of_text(self, text, encoding="utf-8"):
        """Use default hash method to return hash value of a piece of string
        default setting use 'utf-8' encoding.
        """
        m = self.hash_algo()
        m.update(text.encode(encoding))
        if self.return_int:
            return int(m.hexdigest(), 16)
        else:
            return m.hexdigest()

    def of_pyobj(self, pyobj):
        """Use default hash method to return hash value of a piece of Python
        picklable object.
        """
        m = self.hash_algo()
        m.update(pickle.dumps(pyobj, protocol=self.pk_protocol))
        if self.return_int:
            return int(m.hexdigest(), 16)
        else:
            return m.hexdigest()

    def of_file(self, abspath, nbytes=0, chunk_size=1024):
        """Use default hash method to return hash value of a piece of a file

        Estimate processing time on:

        :param abspath: the absolute path to the file
        :param nbytes: only has first N bytes of the file. if 0, hash all file

        CPU = i7-4600U 2.10GHz - 2.70GHz, RAM = 8.00 GB
        1 second can process 0.25GB data

        - 0.59G - 2.43 sec
        - 1.3G - 5.68 sec
        - 1.9G - 7.72 sec
        - 2.5G - 10.32 sec
        - 3.9G - 16.0 sec

        ATTENTION:
            if you change the meta data (for example, the title, years 
            information in audio, video) of a multi-media file, then the hash 
            value gonna also change.
        """
        if nbytes < 0:
            raise ValueError("chunk_size cannot smaller than 0")
        if chunk_size < 1:
            raise ValueError("chunk_size cannot smaller than 1")
        if (nbytes > 0) and (nbytes < chunk_size):
            chunk_size = nbytes

        m = self.hash_algo()
        with open(abspath, "rb") as f:
            if nbytes:  # use first n bytes
                have_reads = 0
                while True:
                    have_reads += chunk_size
                    if have_reads > nbytes:
                        n = nbytes - (have_reads - chunk_size)
                        if n:
                            data = f.read(n)
                            m.update(data)
                        break
                    else:
                        data = f.read(chunk_size)
                        m.update(data)
            else:  # use entire content
                while True:
                    data = f.read(chunk_size)
                    if not data:
                        break
                    m.update(data)

        return m.hexdigest()


fingerprint = FingerPrint()
