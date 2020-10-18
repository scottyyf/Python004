#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: scrapy_battle.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import requests
import time
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    'User-Agent': ua.random,
    'Referer':
        'https://accounts.douban.com/passport/login_popup?login_source=anony',
    }

ss = requests.session()

url = 'https://accounts.douban.com/j/mobile/login/basic'

form_data = {
    "ck": "",
    "remember":	"true",
    "name":	"17503034816",
    "password":	"R00T@hadev"
    }


def main():
    ret = ss.post(url, data=form_data, headers=headers)
    print(ret.cookies)
    ss.close()


if __name__ == "__main__":
    main()
