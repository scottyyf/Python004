#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: glance_scrapy.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import scrapy


class QuotaSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com'
        ]

    def parse(self, response, **kwargs):
        for quota in response.css('div.quote'):
            yield {
                'author': quota.xpath('span/small/text()').get(),
                'test': quota.css('span.text::text').get(),
                }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)