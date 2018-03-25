import cgi
import chardet
import logging
import os
import re
import urllib
from crawler.items import TestItem
from crawler.blacklist import blacklist
from scrapy import signals
from scrapy.http import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from six.moves.urllib.parse import urlparse

logging.config.fileConfig(fname="logging.conf", disable_existing_loggers=False)
ignore_logger = logging.getLogger("ignore_logger")

class GeneralSpider(Spider):
    # The first one is a description for moving Scrapy itself
    name = 'crawler'

    deny_domain_list = []
    deny_list = []

    blist = blacklist(os.path.dirname(os.path.abspath(__file__)) + '/../../txt/blacklist.txt')
    deny_list.extend(blist)

    def __init__(self, *args, **kwargs):
        super(GeneralSpider, self).__init__(*args, **kwargs)
        self.le = LinkExtractor(
            deny=self.deny_list,
            deny_domains=self.deny_domain_list,
        )

    def parse(self, response):
        if (not isinstance(response, HtmlResponse)) or response.status != 200:
            return

        # Extract the URL from the returned HTML and issue the next request
        for link in self.le.extract_links(response):

            r = Request(url=link.url,
                    callback=self.parse,
                )
            r.meta.update(link_text=link.text)
            yield r

        # The parsing part of the returned HTML
        item = TestItem()
        url = response.url
        item['url'] = url
        item['response'] = res
        yield item

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GeneralSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider._set_crawler(crawler)
        spider.crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider
    
    def spider_idle(self):
        self.log("Spider idle signal caught.")
        raise DontCloseSpider
