#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: urls.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converter=converters.IntConverter, type_name='myint')
register_converter(converter=converters.FourDigitYearConverter,
                   type_name='fourdigit')

urlpatterns = [
    # path('<int:year>', views.index),
    path('', views.anydex),
    path('2020', views.x2020),
    # re_path('(?P<year>.*)', views.err, name='years'),
    path('<fourdigit:years>', views.err, name='years'),
    path('books', views.books),
    # path('<myint:years>', views.err, name='years')
]

