#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: multiprocess_queue.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import multiprocessing
import time


def send(q):
    for i in range(10):
        q.put(i)
        time.sleep(0.5)


def load(q: multiprocessing.Queue):
    try:
        while True:
            value = q.get(True, 5)
            print(value)
            if value == 4:
                assert False
    except (ValueError, AssertionError):
        pass

    print('load function ended')


def main():
    q = multiprocessing.Queue()
    ps = multiprocessing.Process(target=send, args=(q,))
    pl = multiprocessing.Process(target=load, args=(q,))
    ps.start()
    pl.start()

    ps.join()
    pl.join()

    print(f'parent process terminated')


if __name__ == "__main__":
    main()
