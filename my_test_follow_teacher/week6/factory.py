#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: factory.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


def fac(func):
    class kclass: pass

    setattr(kclass, func.__name__, classmethod(func))
    return kclass


def say_no():
    print('bar')


# Foo = fac(say_no)
# foo = Foo()
# foo.say_no()

# Fox = type('Fox', (), {'hi':say_no})
# fox = Fox()
# fox.hi()


def pop_value(self, d_value):
    for k in self.keys():
        if self[k] == d_value:
            self.pop(k)
            break


class DelValue(type):
    def __new__(cls, name, bases, attrs, *args, **kwargs):
        attrs['pop_value'] = pop_value
        return type.__new__(cls, name, bases, attrs)


class DelDictV(dict, metaclass=DelValue):
    pass


d = DelDictV()
d['a'] = 'A'
d['b'] = 'B'

d.pop_value('B')

for k, v in d.items():
    print(k, '   : ', v)