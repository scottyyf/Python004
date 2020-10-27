#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: sklearn_test.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

from sklearn import datasets

iris = datasets.load_iris()
x, y = iris.data,  iris.target


# print(x)
# print(y)
#
# print(iris.feature_names)
#
# print(iris.target_names)

from sklearn.model_selection import train_test_split
x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.25)
print(x_tr)
print(x_te)

print(y_tr)
print(y_te)

