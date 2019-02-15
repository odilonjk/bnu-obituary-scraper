# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BnuObituaryScraperSpider(CrawlSpider):
    name = 'bnu-obituary-scraper'
    allowed_domains = ['omunicipioblumenau.com.br']
    start_urls = ['https://omunicipioblumenau.com.br/']

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=('//a[re:test(@href, "obituario")]')
            )
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths=('//div[@class="td-block-span6"]//div[@class="item-details"]/h3/a')
            ),
            callback='parse_new'
        )
    )

    def parse_new(self, response):
        deceased_people = response.xpath('//div[@class="td-post-content"]/p/span[contains(text(), "sepultad")]/text()').getall()
        for deceased in deceased_people:
            deceased_info = deceased.split(',')
            name = deceased_info[0]
            age = deceased_info[1].strip()
            buried_in = deceased_info[2].strip()[deceased_info[2].index('m '):].strip().strip('.')
            yield {
                'name': name,
                'age': age,
                'buried_in': buried_in
            }
