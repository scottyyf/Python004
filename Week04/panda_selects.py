#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: panda_selects.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import pandas as pd

df = pd.read_csv('example.csv')
df1 = pd.read_csv('example1.csv')

# SELECT * FROM data;
print(df)

# SELECT * FROM data LIMIT 10;
print(df.head(10))

# SELECT id FROM data;  //id 是 data 表的特定一列
print(df['id'])

# SELECT COUNT(id) FROM data;
print(df['id'].count())

# SELECT * FROM data WHERE id<1000 AND age>30;
print(df[(df['id'] < 1000) & (df['age'] > 30)])

# SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
# TODO

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
print(df.join(df1, how='inner', on='id'))

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
print(pd.concat([df, df1], axis=0).drop_duplicates())

# 9. DELETE FROM table1 WHERE id=10;
# print(df[(df['id'] != 10).all(axis=0)])
print(df[df['id'] != 10])

# 10. ALTER TABLE table1 DROP COLUMN column_name;
print(df.drop(columns=['column_name'], axis=1))
