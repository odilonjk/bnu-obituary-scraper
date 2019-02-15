# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BnuObituaryScraperSpider(CrawlSpider):
    name = 'bnu-obituary-scraper'

    custom_settings = {
        'BOT_NAME': 'bnu_obituary_scraper',
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/65.0',
        'ROBOTSTXT_OBEY': False,
    }

    allowed_domains = ['arvorespelavida.org.br']
    start_urls = ['https://www.arvorespelavida.org.br/']

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=('//div/ul[@class="menu"]/li/a[re:test(@href, "obituario")]')
            )
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths=('//div[@class="obituario-inner"]/a')
            ),
            callback='parse_new'
        )
    )

    def parse_new(self, response):
        content = response.xpath('//div[@class="content-inner"]')

        name = content.xpath('//p[@class="info-nome"]/text()').get()
        info = content.xpath('//ul[@class="info-dados"]/li/text()').getall()
        age = info[0].strip().split(' ')[0]
        death_date = info[1].strip()
        burial_date = info[2].strip()
        # funeral_place =
        # funeral_coordinates =
        # burial_place =
        # burial_coordinates =
        yield {
            'name': name,
            'age': age,
            'death_date': death_date,
            'burial_date': burial_date
        }
