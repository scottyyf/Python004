#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: multiprocess_class_impl.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import multiprocessing
import os
import time


class NewProcess(multiprocessing.Process):
    def __init__(self, num):
        self.num = num
        super().__init__(name=f'scott-{self.num}')

    def run(self):
        print(self.name)
        print(f'name of process {self.num}')
        print(f'pid is {os.getpid()}')
        time.sleep(2)
        print('*' * 20)
        print()


for i in range(2):
    p = NewProcess(i)
    p.start()
    p.join()
    # print(p.name)
