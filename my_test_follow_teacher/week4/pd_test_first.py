#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: pd_test_first.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import pandas as pd
import numpy as np
import matplotlib as plt
import os

pwd = os.path.dirname((os.path.abspath(__file__)))
book = os.path.join(pwd, 'book_utf8.csv')

df = pd.read_csv(book)
# print(df[1:3])
# 加头
df.columns = ('star', 'vote', 'shorts')

# 行， 列指定
print(df.loc[1:3, 'star'])

# 过滤，excel筛选
print(df['star'] == '力荐')

# 缺失数据
df.dropna()
# print(df)

## 数据聚合
print(df.groupby('star').sum())

# 创建新列
star_to_num = {
    '力荐': 7,
    '很差': 2,
    '推荐': 3,
    '较差': 14,
    '还行': 24
    }
df.columns.__add__(['num_star'])

# python 和excel结合
df['num_star'] = df['star'].map(star_to_num)
print(df)
