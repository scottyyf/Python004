import os

import scrapy
from scrapy.selector import Selector
from ..items import SpidersItem

LIMIT = 10


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response, **kwargs):
        items = []
        selector = Selector(response=response)

        my_xpath = '//div[@class="movie-item-hover"]/a/div[' \
                   '@class="movie-hover-info"]'
        movies_info = selector.xpath(my_xpath)
        for i in movies_info[:LIMIT]:
            item = SpidersItem()
            name = ''.join(i.xpath('./div[1]/span/text()').extract()).strip()
            movie_type = ''.join(i.xpath('./div[2]/text()').extract()).strip()
            show_time = ''.join(i.xpath('./div[4]/text()').extract()).strip()
            item['name'] = name
            item['movie_type'] = movie_type
            item['show_time'] = show_time
            items.append(item)

        return items
