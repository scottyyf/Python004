#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: homework3.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
from functools import wraps
import time
import random


def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start_at = time.monotonic()
        ret = func(*args, **kwargs)
        end_at = time.monotonic()
        print(f'function {func.__name__} spend {end_at - start_at} '
              f'seconds to end')
        return ret

    return inner


@timer
def test(var1, var2, var3=None):
    time.sleep(random.random()*4)


if __name__ == '__main__':
    test(1, 2, 100)
