#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: handle_null_and_dumplicate_value.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import pandas as pd
import numpy as np

x = pd.Series([1, 2, np.nan, 3, 4, 6, np.nan])
# 是否由缺失
print(x.hasnans)

#
print(x.mean())

# 填充值,不改变原来值
print(x.fillna(value=x.mean()))
print(x)

# Dataframe
df = pd.DataFrame(
    {"a": [5, 3, None, 4],
     'b': [None, 2, 4, 3],
     'c': [4, 3, 8, 5],
     'd': [5, 4, 2, None]}
    )
# print(df)
print(df.isnull())
print(df.isnull().sum())
