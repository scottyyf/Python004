#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: webdriver_test.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


from selenium import webdriver

br = webdriver.Chrome()

br.get('https://movie.douban.com/subject/1292052/')


bt1 = br.find_element_by_xpath(
    '/html/body/div[3]/div[1]/div[3]/div[1]/div[10]/div[2]/div[2]/div[1]/a')
bt1.click()

bt2 = br.find_element_by_xpath('//*[@id="paginator"]/a')
bt2.click()

print(br.page_source)

# br.switch_to.frame(br.find_element_by_tag_name('iframe')[0])
# bt2 = br.find_element_by_xpath(
#     '//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]')
# bt2.click()
#
# br.find_element_by_xpath('//*[@id="username"]').send_keys('17503034816')
# br.find_element_by_id('password').send_keys('R00T@hadev')
#
# br.find_element_by_xpath(
#     '//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click()

# cookies = br.get_cookies()
# print(cookies)
br.close()