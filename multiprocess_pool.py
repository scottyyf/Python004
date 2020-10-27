#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: multiprocess_pool.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import multiprocessing
import random
import time
import os


def run(name):
    print(f'child process [{name}] start')
    print(f'os pid is {os.getpid()}')
    time.sleep(random.choice(range(5)))
    print(f'child process [{name}] end *******')


print(f'parent process start')
p = multiprocessing.Pool(multiprocessing.cpu_count())

for i in range(10):
    p.apply_async(run, args=(i,))
    print("*****",len(multiprocessing.active_children()))


p.close()
p.join()
print(f'parent process end')
# p.close()