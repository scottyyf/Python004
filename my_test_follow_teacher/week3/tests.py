import requests
import threading
import json
from queue import Queue
import fake_useragent
from lxml.etree import HTML

ua = fake_useragent.UserAgent()


class Craw(threading.Thread):
    def __init__(self, name, q: Queue, data: Queue):
        super().__init__()
        self.name = name
        self.q = q
        self.data = data

    def run(self) -> None:
        print(f'start craw thread: {self.name}')
        self.scheduler()
        print(f'end craw thread: {self.name}')

    def scheduler(self):
        while True:
            if self.q.empty():
                print(f'self.q is empty? [{self.q.empty()}]')
                self.data.put('end now')
                break

            else:
                page = self.q.get()
                print(f'download thread is : {self.name}, download '
                      f'page is : {page}')
                url = f'https://book.douban.com/top250?start={25 * page}'
                headers = {'User-Agent': ua.random}
                try:
                    rsp = requests.get(url, headers=headers)
                    self.data.put(rsp.text)
                except Exception as e:
                    print(f'Failed for download thread {self.name}: {e}')


class Parser(threading.Thread):
    def __init__(self, name, data_q: Queue, files):
        super().__init__()
        self.name = name
        self.data_q = data_q
        self.files = files

    def run(self) -> None:
        while True:
            print(f'parse thread: {self.name}')
            item = self.data_q.get()
            if item == 'end now':
                break

            self.parse(item)

        print(f'end parse thread: {self.name}')

    def parse(self, item: str):
        selector = HTML(item)
        title_path = '//div[@class="pl2"]'
        books = selector.xpath(title_path)
        for book in books:
            name = book.xpath('./a/text()')
            link = book.xpath('./a/@href')
            resp = {
                'name': name[0].strip(),
                'link': link[0].strip()
                }
            try:
                print(resp)
            except Exception as e:
                print(f'book error: {e}')


if __name__ == '__main__':
    fp = open('scott_test.log', 'w', encoding='utf-8')

    data_que = Queue()

    web_queue = Queue(20)
    for page in range(13):
        web_queue.put(page)

    crawl_total_threads = []
    crawl_names = ['c1', 'c2', 'c3']
    for n in crawl_names:
        c_th = Craw(n, web_queue, data_que)
        c_th.start()
        crawl_total_threads.append(c_th)

    #
    parse_total_thread = []
    parse_names = ['p1', 'p2', 'p3']
    for name in parse_names:
        p_th = Parser(name, data_que, fp)
        p_th.start()
        parse_total_thread.append(p_th)
    #
    for t in parse_total_thread:
        t.join()

    for t in crawl_total_threads:
        t.join()
    #
    fp.close()
    print('exit')
