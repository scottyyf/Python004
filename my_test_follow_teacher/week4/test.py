#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: test.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# df = pd.DataFrame({
#     'Name': ['braund, Mr.Owen Harris',
#              'Allen, mr. William Henry',
#              'Bonnell, Miss.Elizabeth'],
#     'Age': [42, 35, 58],
#     'Sex': [22,45,67]
#     })

# df = pd.read_csv('book_utf8.csv')
# # print(df.values)
# df.iloc[:, 2] = np.nan
# df.columns = [1, 2, 3]
#
# print(df[[1, 2]])
# print(df.loc[1:2])
# print(df)
# # print(df.sum())
# # print(df.min())
# # print(df.max())
# print(df['Age'].idxmin())


# ret = df.ffill(axis=1)
# print(df.isnull().sum())

group = ['x', 'y', 'z']
data1 = pd.DataFrame(
    {
        'group': [group[x] for x in np.random.randint(0, len(group), 10)],
        'salary': np.random.randint(5, 50, 10),


        }
    )

data2 = pd.DataFrame(
    {
        'group': [group[x] for x in np.random.randint(0, len(group), 10)],
        'age': np.random.randint(5, 50, 10),

        }
    )

df = pd.read_csv('James_Harden.csv')

# df = df.fillna(value='0')

ret = pd.pivot_table(df, index=[u'主客场'],values=[u'得分',u'助攻',u'篮板'],
                     columns=['胜负'],fill_value=0, aggfunc=[np.sum])
ret=ret.fillna(value=0)
# print(df)
# ret.to_excel('harden.xlsx', sheet_name='Nba', index=False)


# print(ret)

# plt.plot(df.index, df['胜负'])
# plt.show()
