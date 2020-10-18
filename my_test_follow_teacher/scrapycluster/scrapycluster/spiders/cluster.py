import json

import scrapy

from ..items import \
    ScrapyclusterItem


class ClusterSpider(scrapy.Spider):
    name = 'cluster'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    def parse(self, response):
        print(f"origin ip is {json.loads(response.text)['origin']}")
        item = ScrapyclusterItem()
        item['ip'] = json.loads(response.text)['origin']
        print(f"item to pipeline is {item}")
        yield item
