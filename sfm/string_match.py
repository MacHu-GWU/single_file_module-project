# -*- coding: utf-8 -*-

from fuzzywuzzy import process


def choose_best(text, choice, criterion=None):
    result, confidence_level = process.extractOne(text, choice)
    if criterion is None:
        return result
    elif confidence_level >= criterion:
        return result
    else:
        return None
