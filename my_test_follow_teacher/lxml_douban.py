#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: lxml_douban.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import lxml
from lxml.etree import HTML


from request_douban import get_response


def parse_xml(xpath=None):
    if not xpath:
        xpath = '//*[@id="info"]/span[10]'

    response = get_response('https://movie.douban.com/subject/1292052/')
    if not response:
        return

    selector = HTML(response.text)
    show_time = selector.xpath(xpath + '/text()')
    film_name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')
    rating_score = selector.xpath(
        '//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
    return film_name, show_time, rating_score


def main():
    name, time, score = parse_xml()
    print(name[0], time[0], score[0])


if __name__ == '__main__':
    main()
