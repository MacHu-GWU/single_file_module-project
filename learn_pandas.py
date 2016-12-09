#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np, pandas as pd

n = 1000
df = pd.DataFrame()
df["id"] = range(1, n + 1)
df["type"] = np.random.randint(1, 10, 1000)

data = [
    (1, 1, 0.1),
    (2, 2, 0.2),
    (3, 1, 0.3),
    (4, 2, 0.4),
]
