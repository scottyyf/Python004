#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: pandas_series.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import pandas as pd
import numpy as np

# series可被理解为单列
r = pd.Series(['a', 'b', 'c'])
# print(r)
# print(r[0])

# 通过字典创建带索引的series
s2 = pd.Series({'a': 11, 'b': 22, 'c': 33})
# print(s2)

# 通过关键字index创建带索引的series
s3 = pd.Series([11, 22, 33], index=['a', 'b', 'c'])
# print(s3)

# 数据操作
# print(s3.index)
# print(s3.values)

# PANDAS到python的转换
v = s3.values
print(v.tolist())

# pandas带索引，加快

#map
email = pd.Series(['abc at amazon.com', 'admin@163.com', 'mat@abc.com'])
import re
pattern = '[A-Za-z0-9._]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,5}'
mask = email.map(lambda x: bool(re.match(pattern, x)))
print(mask)
print(email[mask])