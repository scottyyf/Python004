#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: request_douban.py
Author: Scott Yang(Scott)
Email:
Copyright:
Description:
"""

import requests
from bs4 import BeautifulSoup as bs

USER_AGENT = 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'

DOUBAN_URL = 'https://movie.douban.com/top250'


def set_header():
    header = {}
    header.setdefault('user-agent', USER_AGENT)
    return header


def parse_index(index):
    bs_info = bs(index, features='html.parser')

    movies = []
    for tags in bs_info.find_all('div', {'class': 'hd'}):
        for tag in tags.find_all('a', ):
            movies.append((tag.get('href'),
                           tag.find('span', {'class': 'title'}).text,
                           tag.find('span', {'class': 'other'}).text.replace(
                               '\xa0', ''))
                          )
    return movies


def get_response(url=DOUBAN_URL, **kwargs):
    header = set_header()
    response = requests.get(url, headers=header, timeout=10,
                            **kwargs)
    if response.ok:
        return response

    return None


def get_top250_info():
    movies = []
    for start in range(10):
        response = get_response(params={'start': start * 25, 'filter': ''})
        if not response:
            break

        movie = parse_index(response.text)
        movies.extend(movie)

    return movies


def main():
    top_info = get_top250_info()
    for movie in top_info:
        print(f'URL: [{movie[0]}]\tMOVIE: [{movie[1]}]\t\t\t\t\tDESC: [{movie[2]}]')


if __name__ == '__main__':
    """
        //*[@id="info"]/span[10]
    """
    main()
