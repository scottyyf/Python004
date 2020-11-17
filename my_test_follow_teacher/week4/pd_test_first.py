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

from snownlp import SnowNLP

pwd = os.path.dirname((os.path.abspath(__file__)))
book = os.path.join(pwd, 'book_utf8.csv')

df = pd.read_csv(book)

df.columns = ('star', 'vote', 'shorts')

star_to_number = {
    '力荐' : 5,
    '推荐' : 4,
    '还行' : 3,
    '较差' : 2,
    '很差' : 1
}

df['new_star'] = df.star.map(star_to_number)

first_line = df[df['new_star'] == 3].iloc(axis=0)[0]
text = first_line.shorts


def _get_sentiment(text):
    s = SnowNLP(text)
    return s.sentiments


df['sentiment'] = df.shorts.apply(_get_sentiment)
print(df.sentiment.mean())


