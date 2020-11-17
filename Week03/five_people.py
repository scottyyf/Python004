#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: five_people.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import threading
import random
import time
from datetime import datetime
from queue import Queue
import sys


class ThinkAndEat(threading.Thread):
    def __init__(self, boy_name, left_lock: threading.Lock,
                 right_lock: threading.Lock,
                 data: Queue,
                 rice_lock: threading.Lock,
                 void_dead_lock: Queue,
                 index=1,
                 times=1,
                 ):
        super().__init__()
        self.boy_name = boy_name
        self.left_lock = left_lock
        self.right_lock = right_lock
        self.times = times
        self.index = index
        self.data = data
        self.rice_lock = rice_lock
        self.dead_lock = void_dead_lock
        self.ticket = None

    def run(self) -> None:
        total = 0
        while total < self.times:
            self.go_think()
            self.try_to_get_ticket()
            self.try_to_get_fork()
            self.go_eat()
            self.drop_fork()
            self.drop_ticket()
            total += 1

    def try_to_get_ticket(self):
        if self.ticket:
            print(f'{self.boy_name} alread have ticket')
            return True

        self.ticket = self.dead_lock.get(True)
        print(f'{self.boy_name} successfully get ticket')
        return True

    def drop_ticket(self):
        self.ticket = None
        self.dead_lock.put('x_mark')

    def try_to_get_fork(self):
        self._get_fork(self.left_lock, 'left fork')
        self._get_fork(self.right_lock, 'right fork')

    def _get_fork(self, locks, which):
        while True:
            if locks.locked():
                time.sleep(random.uniform(1, 3))
                continue

            print(f'{self.boy_name} get {which} at '
                  f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')
            locks.acquire()
            if which == 'left fork':
                self.data.put([self.index, 1, 1])
            else:
                self.data.put([self.index, 2, 1])

            break

    def drop_fork(self):
        self.left_lock.release()
        self.data.put([self.index, 1, 2])
        self.right_lock.release()
        self.data.put([self.index, 2, 2])
        print(f'{self.boy_name} drop fork at '
              f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')

    def go_think(self):
        print(f'{self.boy_name}: run into thinking state!')
        time.sleep(random.randint(1, 3))
        print(f'{self.boy_name}: out of thinking state')

    def go_eat(self):
        print(f'{self.boy_name} eat rice with lock')
        while True:
            if self.rice_lock.locked():
                print(f'{self.boy_name} says: some one is in eating state, '
                      f'i will wait')
                time.sleep(random.randint(0, 1))
                continue

            self.rice_lock.acquire()
            self.data.put([self.index, 0, 3])
            print(f'{self.boy_name}: run into eating state at '
                  f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')
            time.sleep(random.randint(1, 3))
            self.rice_lock.release()
            break


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        TIME = 1
    else:
        TIME = int(args[1])

    five_guys = ['Scott', 'Lucy', 'Mary', 'Tom', 'mark']
    locks = [threading.Lock() for _ in range(5)]
    rice_lock = threading.Lock()
    void_dead_lock = Queue(4)
    for _ in range(4):
        void_dead_lock.put('x_mark')

    data = Queue()
    ret = [
        ThinkAndEat(
            five_guys[i], locks[i], locks[(i + 1) % 5], data, rice_lock,
            void_dead_lock, index=i + 1, times=TIME, ) for i in range(5)]
    for t_and_e in ret:
        t_and_e.setDaemon(True)
        t_and_e.start()

    for t_and_e in ret:
        t_and_e.join()

    print()
    print()
    print("*" * 50)
    print("*" * 50)

    for _ in range(data.qsize()):
        print(data.get())
