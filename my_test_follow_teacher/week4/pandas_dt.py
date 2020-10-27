#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: pandas_dt.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import pandas as pd

df1 = pd.DataFrame(['a', 'b', 'c', 'd'])
print(df1)

df2 = pd.DataFrame([['a', 'b'], ['c', 'd']])
df2.columns = ['one', 'two']
df2.index = ['first', 'second']
print(df2)

print(df2.columns)
print(df2.index)
print(type(df2.values))
