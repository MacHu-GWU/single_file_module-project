#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fuzzywuzzy import process


def choose_best(text, choice, criterion=None):
    if criterion is None:
        return choose_best(text, choice, criterion=0)
    else:
        res, confidence_level = process.extractOne(text, choice)
        if confidence_level >= criterion:
            return res
        else:
            return None
