#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: threading_test.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import threading
import os
import queue
import time


def run(n):
    print(f'pid is {os.getpid()}')
    print(n)


def main1():
    t1 = threading.Thread(target=run, args=('thread 1',))
    t2 = threading.Thread(target=run, args=('thread 2',))
    t1.start()
    t2.start()


class MyThread(threading.Thread):
    def __init__(self, n):
        super().__init__()
        self.n = n

    def run(self):
        print(f'task is {self.n}')


def main2():
    t1 = MyThread('1')
    t2 = MyThread('2')
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(t1.getName())


def main3():
    q = queue.Queue(5)
    q.put(111)
    q.put(222)
    q.put(333)

    print(q.get())
    print(q.get())
    q.task_done()

    print(q.qsize())
    print(q.empty())
    print(q.full())


l1 = threading.Lock()

import random


class Producer(threading.Thread):
    def __init__(self, queue: queue.Queue, con: threading.Condition, name):
        super().__init__()
        self.q = queue
        self.con = con
        self.name = name

    def run(self) -> None:
        while True:
            global l1
            self.con.acquire()

            if self.q.full():
                print(f'{self.name} queue is full, producer wait')

                self.con.wait()

            else:
                value = str(random.randint(1, 10))
                print(f'{self.name} put value {value} to {self.name}')
                self.q.put(f'{self.name}: {value}')
                self.con.notify()
                time.sleep(1)

        self.con.release()


class Consumer(threading.Thread):
    def __init__(self, q: queue.Queue, con: threading.Condition, name):
        super().__init__()
        self.name = name
        self.con = con
        self.q = q

    def run(self) -> None:
        while True:
            global l1
            self.con.acquire()

            if self.q.empty():
                print('queue is empty, consumer wait')

                self.con.wait()

            else:
                value = self.q.get()
                print(f'{self.name} get value {value}')

                self.con.notify()
                time.sleep(1)

        self.con.release()


def main():
    q = queue.Queue(4)
    th1 = threading.Condition()
    c1 = Consumer(q, th1, 'c1')
    c1.start()
    p1 = Producer(q, th1, 'p1')
    p1.start()
    p2 = Producer(q, th1, 'p2')
    p2.start()
    Producer(q, th1, 'p3').start()
    Producer(q, th1, 'p4').start()


main()
