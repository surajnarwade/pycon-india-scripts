import scrapy
from scrapy.crawler import CrawlerProcess


class PySpider(scrapy.Spider):
    name = 'pyconindia'
    start_urls = ['https://in.pycon.org/cfp/2016/proposals/']

    def parse(self, response):
        for href in response.css('.row h3 a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_data)

    def parse_data(self, response):
        yield {
            'title': response.css('.container-fluid h1::text').extract_first(),
            'author': response.css('.container-fluid b::text').extract_first(),
            'link': response.url,
            }

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': 'result.json',
    'LOG_ENABLED': 0
})

process.crawl(PySpider)
process.start()  # the script will block here until the crawling is finished
