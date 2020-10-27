#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: multiprocess_map.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import multiprocessing


def f(x):
    return x * x


with multiprocessing.Pool(processes=4) as pool:
    ret = pool.map(f, range(4))
    print(ret)

    ret = pool.imap(f, range(4))
    print(ret)
    for i in ret:
        print(i)