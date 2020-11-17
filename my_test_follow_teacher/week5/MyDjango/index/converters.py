#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: converters.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


class IntConverter:
    regex = '[0-9]+'

    def to_python(self, value):
        if int(value) > 200:
            return 200

        return int(value)

    def to_url(self, value):
        # return str(value)
        return '1211'


class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
