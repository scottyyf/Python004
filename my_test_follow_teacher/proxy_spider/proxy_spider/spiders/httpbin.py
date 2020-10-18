import scrapy
'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware'

class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    def parse(self, response):
        print(response.text)
