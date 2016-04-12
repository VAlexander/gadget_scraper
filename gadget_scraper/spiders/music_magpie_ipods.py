# -*- coding: utf-8 -*-

from scrapy import Spider, Request, FormRequest
from scrapy.selector import Selector
import json
try:
	from items import GadgetScraperItem
except ImportError:
	from gadget_scraper.items import GadgetScraperItem

class MusicMagpieIpodsSpider(Spider):
	name = "music_magpie_ipods"
	allowed_domains = ["musicmagpie.co.uk"]
	start_urls = ("http://www.musicmagpie.co.uk",)

	def parse(self, response):
		formdata={
			"category": "Model",
			"knownCategoryValues": "undefined:iPod;Make:Apple;",
		}
		
		request = Request(
			url="http://www.musicmagpie.co.uk/usercontrols/techService.asmx/GetModels",
			method='POST', 
			body=json.dumps(formdata),			
			headers={"Content-Type": "application/json; charset=UTF-8"},
			meta={"make": "Apple"},
			callback=self.parse_ipods_models,
			)
		
		yield request
		
	def parse_ipods_models(self, response):
		json_response = json.loads(response.body)
		
		for ipod_entry in json_response["d"]:
			item = GadgetScraperItem()
			model = ipod_entry["name"].strip()
			
			item["make"] = response.meta["make"]
			item["model"] = model
			
			yield item