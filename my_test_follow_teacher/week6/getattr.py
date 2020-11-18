#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: __init__.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


class Human:
    def __init__(self):
        self.name = 's'

    def __get__(self, instance, owner):
        # print(instance.dirname)
        print('get')
        return self.name

    def __set__(self, instance, value):
        print('set')
        self.name = value

    def __delete__(self, instance):
        print('del')


class my:
    a = Human()


a = my()
# print(a.a)
a.a = 10
print(a.a)
# del(a.a)

import os


def single(cls):
    instances = {}

    def get_ins():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_ins


@single
class MyClass:
    pass


class Foo:
    SINGLE = None

    def __new__(cls, *args, **kwargs):
        if cls.SINGLE:
            return cls.SINGLE

        cls.SINGLE = super().__new__(cls)
        return cls.SINGLE

    def __init__(self):
        self.name = 's'

# f = Foo()
# f1 = Foo()
# print(id(f))
# print(id(f1))
#
# print(id(os.name))
# print(id(os.name))
