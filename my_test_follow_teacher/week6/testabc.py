#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: testabc.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


# from abc import ABCMeta, abstractmethod, ABC, get_cache_token
#
# class Base(ABC):
#     @abstractmethod
#     def foo(self):
#         pass
#
#
# class Concrete(Base):
#     def __init__(self):
#         pass
#
#     def foo(self):
#         pass
#
#
# c = Concrete()
# print(get_cache_token())


class Display():
    def display(self, message):
        print(message)


class LoggerMixin():
    def log(self, message, filename='logfile.txt'):
        with open(filename, 'a') as fh:
            fh.write(message)

    def display(self, message):
        super().display(message)
        self.log(message)


class MysubClass(LoggerMixin, Display):
    def log(self, message):
        super().log(message, filename='subclass.txt')


sub_class = MysubClass()
sub_class.display('this is subclass display')
print(MysubClass.mro())
