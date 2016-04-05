# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest
from scrapy.selector import Selector
from gadget_scraper.items import GadgetScraperItem
import json


class TestSpider(Spider):
	name = "test"
	allowed_domains = ["comparemymobile.com"]
	start_urls = (
		'http://www.comparemymobile.com/sell/ipad',
	)

	def parse(self, response):
		for stage_1_link in response.xpath("//div[@class='stage1']/ul/li/a/@data-group0").extract():
			yield FormRequest(
				url="http://www.comparemymobile.com/ajax-data",
				formdata={
					"task": "group0",
					"manufacturer": "159",
					"category": "7",
					"group": stage_1_link
					},
				callback=self.get_stage_2
				)
			
	
	def get_stage_2(self, response):
		j = json.loads(response.body)
		for i in j["items"]:
			yield FormRequest(
				url="http://www.comparemymobile.com/ajax-data",
				formdata={
					"task": "group1",
					"manufacturer": "159",
					"category": "7",
					"group": i["group1"]
					},
				callback=self.get_stage_3
				)
			
	def get_stage_3(self, response):
		j = json.loads(response.body)
		for i in j["items"]:
			yield FormRequest(
				url="http://www.comparemymobile.com/ajax-data",
				formdata={
					"task": "group2",
					"manufacturer": "159",
					"category": "7",
					"group1": i["group1"],
					"group": i["group2"]
					},
				callback=self.get_stage_4
				)
				
	def get_stage_4(self, response):
		j = json.loads(response.body)
		for i in j["items"]:
			print i["url"]