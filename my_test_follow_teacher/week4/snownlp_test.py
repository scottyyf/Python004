#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: snownlp_test.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import pandas as pd
import jieba
from snownlp import SnowNLP
df = pd.read_csv('book_utf8.csv')
df.columns = ['star', 'vote', 'shorts']
star_to_number = {
    '力荐': 5,
    '推荐': 4,
    '还行': 3,
    '较差': 2,
    '很差': 1,
    }

df['new_star'] = df['star'].map(star_to_number)

first_line = df[df['new_star'] == 3].iloc[0]
# print(first_line)
text = first_line['shorts']
s = SnowNLP(text)
print(s.sentences)
print(s.sentiments)
print(s.keywords(3))
print(s.pinyin)
print(s.words)

j = jieba.cut(text)
print(list(j))