#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: login_shimo.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import configparser
import os
from selenium import webdriver


class LoginInfo:
    def __init__(self, config_file=''):
        self.config_file = config_file
        self._user = ''
        self._pw = ''
        self._load_config()

    def _load_config(self):
        if not os.path.isfile(self.config_file):
            raise ValueError(f'{self.config_file} is not exist')

        config = configparser.ConfigParser()
        config.read(self.config_file)
        self._user = config['DEFAULT']['user_name']
        self._pw = config['DEFAULT']['password']

    @property
    def pw(self):
        return self._pw

    @property
    def user(self):
        return self._user


class Driver:
    def __init__(self):
        self._safari = None
        self.set_driver()

    def set_driver(self):
        raise NotImplementedError


class ChromeDriver(Driver):
    def set_driver(self):
        self._safari = webdriver.Chrome()

    def run(self):
        raise NotImplementedError


class ShiMo(ChromeDriver):
    def __init__(self, url):
        super().__init__()
        self.url = url
        base_path = os.path.dirname(os.path.abspath(__file__))
        self._config = LoginInfo(os.path.join(base_path, 'login_context.txt'))
        self.user = self._config.user
        self.pw = self._config.pw

    def run(self):
        self._safari.get(self.url)
        lg = self._safari.find_element_by_xpath(
            '//div[@class="entries"]/a[2]/button')
        lg.click()

        user = self._safari.find_element_by_name('mobileOrEmail')
        user.send_keys(self.user)

        pw = self._safari.find_element_by_name('password')
        pw.send_keys(self.pw)

        com = self._safari.find_element_by_xpath(
            '//button[@class="sm-button submit sc-1n784rm-0 bcuuIb"]')

        com.click()


if __name__ == '__main__':
    shimo = ShiMo('https://shimo.im/')
    shimo.run()
