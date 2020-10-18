#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: request_stream.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import requests

proxies={'http': 'http://192.168.4.61:7890',
         'https': 'https://192.168.4.61:7890'}

image_url = 'https://www.python.org/static/community_logos/' \
            'python-logo-master-v3-TM.png'

# rsp = requests.get(image_url, proxies=proxies)
# with open('python.png', 'wb') as f:
#     f.write(rsp.content)

rsp = requests.get(image_url, proxies=proxies, stream=True)
with open('python2.png', 'wb') as f:
    for chunk in rsp.iter_content(4096, decode_unicode=True):
        f.write(chunk)

rsp.close()
