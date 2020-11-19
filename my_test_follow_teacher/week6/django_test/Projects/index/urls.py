#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: urls.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

from django.urls import path
from . import views

app_name = 'index'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.resutls, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
    ]
