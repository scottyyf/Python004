#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: homework2.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


def fake_map(func, iterable):
    for i in iterable:
        yield func(i)


def test(var):
    return var


if __name__ == '__main__':
    ret = fake_map(test, range(10))
    for i in ret:
        print(i, end=' ')

    print()

    for i in map(test, range(10)):
        print(i, end=' ')