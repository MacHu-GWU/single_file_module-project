#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six
import inspect
from pprint import pprint as ppt

class MyClass(object):
    attr1 = "attribute1"
    attr2 = "attribute2"
    
    def method(self):
        pass
    
    @staticmethod
    def static_method():
        pass
    
    @classmethod
    def class_method(cls):
        pass
    
# user_schema = UserSchema()
# ppt(user_schema.__dict__)

def print_keys(items):
    for key, value in items:
        print(key)

def get_attributes(klass):
    attributes = list()
    for attr, value in inspect.\
        getmembers(klass, lambda x: not inspect.isroutine(x)):
        if not (attr.startswith("__") and attr.endswith("__")):
            attributes.append(attr)
    return attributes

# def get_function():

def get_methods(klass):
    methods = list()
    attributes = get_attributes(klass)
    for key, value in inspect.getmembers(MyClass):
        if (not (key.startswith("__") and key.endswith("__"))) and \
            (key not in attributes):
            methods.append(key)
    return methods

# print_keys(inspect.getmembers(MyClass, lambda x: inspect.isfunction(x))) # method
# print_keys(inspect.getmembers(MyClass, lambda x: inspect.ismethod(x)))

# print_keys(inspect.getmembers(MyClass, lambda x: not inspect.isroutine(x)))
# print_keys(inspect.getmembers(MyClass, lambda x: inspect.isbuiltin(x)))

def test_get_attributes():
    assert get_attributes(MyClass) == ["attr1", "attr2"]

test_get_attributes()

def test_get_methods():
#     assert get_methods(MyClass) == ["method", ""]
    print(get_methods(MyClass))
    
test_get_methods()