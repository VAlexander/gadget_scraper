# -*- coding: utf-8 -*-

from scrapy import Spider

try:
    from items import GadgetScraperItem
except ImportError:
    from gadget_scraper.items import GadgetScraperItem


class MusicMagpieConsolesSpider(Spider):
    name = "music_magpie_consoles"
    allowed_domains = ["musicmagpie.co.uk"]
    start_urls = ()

    def start_requests(self):
        pass
