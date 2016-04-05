# -*- coding: utf-8 -*-

import scrapy

class GadgetScraperItem(scrapy.Item):
	# Main model for the scraper. To be exported in .csv
	make = scrapy.Field()
	model = scrapy.Field()
	working_price_1 = scrapy.Field()
	working_price_2 = scrapy.Field()
	working_price_3 = scrapy.Field()
	working_price_4 = scrapy.Field()
	working_price_5 = scrapy.Field()
	working_price_6 = scrapy.Field()
	broken_price_1 = scrapy.Field()
	broken_price_2 = scrapy.Field()
	broken_price_3 = scrapy.Field()
	broken_price_4 = scrapy.Field()
	broken_price_5 = scrapy.Field()
	broken_price_6 = scrapy.Field()
