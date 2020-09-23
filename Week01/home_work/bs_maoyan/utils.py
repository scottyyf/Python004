#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: utils.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import os
import shutil
import time
from typing import Union, Optional
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

__URL = 'https://maoyan.com/films?showType=3'
__USER_AGENT = 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 ' \
               '(KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
__COOKIE = '__mta=19167879.1601174661233.1601174895258.1601175697001.3; ' \
           'uuid_n_v=v1; uuid=578BC310006B11EBB86FCBED18BA04EA658ED82A12' \
           '6B410D806EF30553458A85; _csrf=acb4b9917f72934d8c626cf5e7e97bd8dd' \
           'd75ef91d1f61bab299d1e673fc584e; ' \
           'mojo-uuid=298574953f55a6a3100126d50' \
           'c2ca339; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1601174661; ' \
           '_lxsdk_cuid=174cd7267c4c8-091558ecac18b4-66313e58-1fa400-1' \
           '74cd7267c4c8; _lxsdk=578BC310006B11EBB86FCBED18BA04EA658ED82A1' \
           '26B410D806EF30553458A85; mojo-session-id={"id":"2ee9c763407f0e65' \
           'a51ec26c5e51fa37","time":1601174661131}; mojo-trace-id=7; Hm_lpv' \
           't_703e94591e87be68cc8da0da7cbd0be2=1601175742; ' \
           '__mta=19167879.1601' \
           '174661233.1601175697001.1601175742059.4; ' \
           '_lxsdk_s=174cd7267c7-491-9' \
           '63-fab%7C%7C11'
MAOYAN_MOVIES_HTML = 'list_maoyans.html'


class Movies:
    """there is a lot of thing can be done in this class, i feel"""
    __slots__ = ['_name', '_movie_type', '_show_time']

    def __init__(self, name, movie_type, show_time):
        self._name = name
        self._movie_type = movie_type
        self._show_time = show_time

    @property
    def to_list(self):
        return [self._name, self._movie_type, self._show_time]


def get_index_data(url=None):
    url = url
    if not url:
        url = __URL

    print(f'Scrapy website {url}...')
    response = requests.get(url, headers={'User-Agent': __USER_AGENT,
                                          'Cookie': __COOKIE}, timeout=10)
    if not response.ok:
        print(f'Failed to get response from {url} with code '
              f'{response.status_code}')
        raise ValueError

    return response


def parse_rsp(response: Union[str, requests.Response], num: Optional[int]):
    # bs_info = bs(response.text)
    if not response:
        return

    content = ''
    if isinstance(response, str):
        content = response

    elif isinstance(response, requests.Response):
        content = response.text

    if not content:
        return

    bs_info = bs(content, features='html.parser')
    all_movies = bs_info.find_all(
        'div', attrs={'class': 'movie-item film-channel'}, limit=num)

    ret = []
    for movie_info in all_movies:

        dumpy_info = movie_info.find_all(
            'div', attrs={'class': 'movie-hover-title'})
        name, movie_type, people, show_time = [x for x in dumpy_info]
        name = name.find(class_='name').get_text()
        movie_type = str(movie_type.find('span').next_sibling).strip()
        show_time = str(show_time.find('span').next_sibling).strip()
        ret.append(Movies(name, movie_type, show_time))

    return ret


def save_to_csv(data: list):
    if not isinstance(data, list):
        raise TypeError

    sum_data = []
    for ret in data:
        sum_data.append(ret.to_list)

    file_name = 'test.csv'

    pds = pd.DataFrame(data=sum_data)
    if os.path.exists(file_name):
        tmp_file = file_name.strip(
            '.csv') + time.strftime('-%Y%m%dT%H%M%S', time.localtime()) + '.csv'
        print(f'backup csv file [{file_name}] to [{tmp_file}]')
        shutil.copy(file_name, tmp_file)

    print(f'save new content to {file_name}')
    pds.to_csv('test.csv', sep='#', header=False, index=False)


def main():
    print(f'Start to scrapy website {__URL}')
    if os.path.exists(MAOYAN_MOVIES_HTML):
        with open(MAOYAN_MOVIES_HTML, 'r') as f:
            rsp = f.read()

    else:
        rsp = get_index_data()
        with open(MAOYAN_MOVIES_HTML, 'w') as f:
            f.write(rsp.text)

        rsp = rsp.text

    # print(rsp)
    ret = parse_rsp(rsp, num=10)
    save_to_csv(ret)


if __name__ == "__main__":
    main()
