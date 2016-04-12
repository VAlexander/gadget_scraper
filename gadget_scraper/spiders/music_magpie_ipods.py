# -*- coding: utf-8 -*-
import scrapy


class MusicMagpieIpodsSpider(scrapy.Spider):
    name = "music_magpie_ipods"
    allowed_domains = ["www.musicmagpie.co.uk"]
    start_urls = (
        'http://www.www.musicmagpie.co.uk/',
    )

    def parse(self, response):
        pass
