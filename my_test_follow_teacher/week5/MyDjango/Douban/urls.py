#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: urls.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
from django.urls import path, include
from . import views


urlpatterns = [
    # path('<int:year>', views.index),
    path('', views.douban),
    path('list', views.book_sort)
]
