#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: panda_douban.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import pandas

from lxml_douban import parse_xml


def main():
    data = parse_xml()
    pd_data = pandas.DataFrame(data=data)
    pd_data.to_csv('./pd_movie.csv', header=False, index=False,
                   encoding='utf-8')


if __name__ == '__main__':
    main()
