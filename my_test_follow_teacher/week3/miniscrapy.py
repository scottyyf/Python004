#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: miniscrapy.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import json
import time
from queue import Queue
import threading
from lxml.etree import HTML

import requests


class CrawlThread(threading.Thread):
    def __init__(self, thread_name, que: Queue, dataqueue: Queue, flag):
        super().__init__()
        self.thread_name = thread_name
        self.que = que
        self.data_que = dataqueue
        self.flag = flag

    def run(self) -> None:
        print(f'start crawl thread: {self.thread_name}')
        self.scheduler()
        print(f'end crawl thread: {self.thread_name}')

    def scheduler(self):
        while True:
            if self.que.empty():
                print('page queue empty, exit scheduler')
                break

            page = self.que.get()
            print(f'downloader thread is: {self.thread_name}, page: {page}')
            url = f'https://book.douban.com//top250?start={page * 25}'
            headers = {
                'user-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/85.0.4183.121 Safari/537.36'
                }
            try:
                response = requests.get(url, headers=headers)
                self.data_que.put(response.text)
            except Exception as e:
                print(f'Failed to download {url}, details: {e}')

        self.flag.flag = False


class ParserThread(threading.Thread):
    def __init__(self, thread_name, que, fd, flag):
        super().__init__()
        self.que = que
        self.thread_name = thread_name
        self.fd = fd
        self.flag = flag

    def run(self) -> None:
        print(f'start parser thread: {self.thread_name}')
        while self.flag.flag:
            try:
                item = self.que.get(False)
                if not item:
                    time.sleep(1)
                    continue

                self.parse_data(item)
                self.que.task_done()
            except Exception as e:
                pass

        print(f'end parser thread: {self.thread_name}')

    def parse_data(self, item):
        try:
            html = HTML(item)
            books = html.xpath('//div[@class="pl2"]')
            for book in books:
                try:
                    titile = book.xpath('./a/text()')
                    link = book.xpath('./a/@href')
                    response = {
                        'title': titile[0].strip(),
                        'link': link[0].strip(),
                        }
                    json.dump(response, fp=self.fd, ensure_ascii=False,
                              indent=4)
                except Exception as e:
                    print(f'book error: {e}')
        except Exception as e:
            print(f'page error: {e}')


class Flag:
    def __init__(self, flag):
        self.flag = flag


def main():
    output = open('book.json', 'a', encoding='utf-8')
    flag = Flag(True)

    dataqueue = Queue()
    pagequeue = Queue(20)
    for page in range(0, 11):
        pagequeue.put(page)

    crawl_threads = []
    crawl_name_list = ['crawl-1', 'crawl-2', 'crawl-3']
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, pagequeue, dataqueue, flag)
        thread.start()
        crawl_threads.append(thread)

    parse_thread = []
    parser_name_list = ['parse-1', 'parse-2', 'parse-3']
    for thread_id in parser_name_list:
        thread = ParserThread(thread_id, dataqueue, output, flag)
        thread.start()
        parse_thread.append(thread)

    for i in crawl_threads:
        i.join()

    for t in parse_thread:
        t.join()

    output.close()
    print('exit parent process')


if __name__ == '__main__':
    main()
   