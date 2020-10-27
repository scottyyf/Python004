#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: fork_test.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import os
import time
import multiprocessing
from multiprocessing import Process
from multiprocessing import active_children


num = 100


def test_fork():
    """
    only support in linux and mac os
    :return:
    """
    ret = os.fork()
    if ret == 0:
        print(f'child process, pid is {os.getpid()}')
    else:
        print(f'parent process {os.getpid()}, child pid is {ret}')


def debug_info(title):
    print("*" * 20)
    print(title)
    print(f'module name is {__name__}')
    print(f'parent pid is {os.getppid()}')
    print(f'current pid is {os.getpid()}')
    print("*" * 20)


def f():
    # debug_info('function f')
    # print(f'hello {name}')
    # time.sleep(2)
    # print(f'goodbye {name}')
    print('child process begin')
    global num
    num += 1
    print(f'child process num: {num}')
    print(f'child process end')


def test_multi_process():
    p = Process(target=f) #, args=('scott',), daemon=True)
    # print('get Start')
    p.start()

    # for x in active_children():
    #     print(f'child is {x.name} , id {x.pid}')

    p.join()
    # print(f'get end, {multiprocessing.cpu_count()}')
    print('parent process end')
    print(f'num is {num}')


def main():
    test_multi_process()


if __name__ == '__main__':
    main()
