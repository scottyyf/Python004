#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: animals.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


class Shape:
    CHOICE = ['slim', 'medium', 'fat']
    # shape = 'slim'

    def __getattribute__(self, item):
        if item != 'shape':
            return ''

        return super().__getattribute__('shape')

    def __setattr__(self, key, value):
        if key != 'shape':
            super().__setattr__(key, value)
            return

        if value not in Shape.CHOICE:
            value = 'slim'

        super().__setattr__('shape', value)


class Food:
    CHOICE = ['meat', 'glass', 'both']
    # type = 'both'

    def __getattribute__(self, item):
        if item != 'type':
            return ''

        return super().__getattribute__('type')

    def __setattr__(self, key, value):
        if key != 'type':
            super().__setattr__(key, value)
            return

        if value not in Food.CHOICE:
            value = 'both'

        super().__setattr__('type', value)


class Character:
    CHOICE = ['gentle', 'violent']
    # character = 'gentle'

    def __getattribute__(self, item):
        if item != 'character':
            return ''

        return super().__getattribute__('character')

    def __setattr__(self, key, value):
        if key != 'character':
            super().__setattr__(key, value)
            return

        if value not in Character.CHOICE:
            value = 'gentle'

        super().__setattr__('character', value)


if __name__ == '__main__':
    c = Character()
    print(c.xo)