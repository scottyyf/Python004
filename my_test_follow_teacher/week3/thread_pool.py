#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: thread_pool.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import re
from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ThreadPoolExecutor

import requests

urls = [
    'https://docs.python.org/zh-cn/3/library/threading.htm',
    'https://docs.python.org/3/library/multiprocessing.html',
    'https://docs.python.org/3/library/functions.html'
    ]

# pool = ThreadPool(4)
# ret = pool.map(requests.get, urls)
#
# pool.close()
# pool.join()
#
# for i in ret:
#     print(i.text)

# with ThreadPoolExecutor(max_workers=3) as exe:
#     # ret = exe.map(requests.get, urls)
#     # for i in ret:
#     #     print(i.url)
#
#     ret = exe.submit(pow, 2, 3)
#     print(ret.result())
from lxml.etree import HTML

file_path = '/home/scott/work/xunjian/巡检分析报告SLES-2020-YYF/待分析数据/DAL-260' \
            '/DAL_BAK_SERV.html'
with open(file_path, 'r') as f:
    content = f.read()

selector = HTML(content)


# ret = selector.xpath('/html/body/table/tr[14]/td[2]/text()')
# if 't when poll reach' in ret[0] and '=====' in ret[1]:
#     c = re.compile(
#         r'(\S*) *(\S*) *(\S*) *(\S]*) *(\S*) *(\S*) *(\S*) *(\S*) *(\S*) *(
#         \S*)')
#     rets = c.search(ret[2].strip())
#     print(ret[2])
#     print(rets.groups())

def dumplicate_check(start_num, xpath_reg: str, step=4):
    """due to html wrong set"""
    start_at = start_num - step
    stop_at = start_num + step + 1
    if start_at < 0:
        start_at = 0

    ret = []
    # '/html/body/table/tr[{0}]/td[2]/text()'
    for i in range(start_at, stop_at):
        if i == start_num:
            continue

        _xpath = xpath_reg.format(i)
        _ret = selector.xpath(_xpath)
        ret.extend(_ret)

    return ret


def risk_ntp_out_scope():
    if selector is None:
        return ''

    ret = selector.xpath('/html/body/table/tr[14]/td[2]/text()')
    _c = re.compile(
        r'(\S*) *(\S*) *(\S*) *(\S]*) *(\S*) *(\S*) *(\S*) *(\S*) *(\S*) *(\S*)')

    ret = _ntp_le_500(ret, _c)
    if ret:
        return ret

    ret = dumplicate_check(
        14, '/html/body/table/tr[{0}]/td[2]/text()', step=5)
    for i in ret:
        result = _ntp_le_500(i, _c)
        if result:
            return result

    return ''


def _ntp_le_500(ret: list, _c):
    if not ret:
        print('not ret')
        return ''

    if len(ret) < 3:
        print(len(ret))
        print('len not >= 3')
        return ''

    if 't when poll reach' not in ret[0] or '===' not in ret[1]:
        print('when poll reach not in ret[0]')
        return ''

    ret = _c.search(ret[2])
    if float(ret.group(9)) >= 0:
        return ret.group(0)

    print('ret.group(9)', ret.group(0))
    return ''

ret = risk_ntp_out_scope()
print(ret)