# -*- coding: utf-8 -*-

import json

from scrapy import Spider, Request, FormRequest

try:
    from items import GadgetScraperItem
except ImportError:
    from gadget_scraper.items import GadgetScraperItem


class MusicMagpieConsolesSpider(Spider):
    name = "music_magpie_consoles"
    allowed_domains = ["musicmagpie.co.uk"]
    start_urls = ()

    def start_requests(self):
        # Initial request to get all makes of consoles
        formdata = {
            "category": "Make",
            "contextKey": "",
            "knownCategoryValues": "undefined:Games Console;",
        }

        request = Request(
            url="http://www.musicmagpie.co.uk/usercontrols/techService.asmx/GetMakes",
            method='POST',
            body=json.dumps(formdata),
            headers={"Content-Type": "application/json; charset=UTF-8"},
            callback=self.parse_consoles_makes,
        )

        return (request,)

    def parse_consoles_makes(self, response):
        # Parsing JSON response with makes
        json_response = json.loads(response.body)

        for make in json_response["d"]:
            # And for each make making request to get models
            formdata = {
                "category": "Model",
                "knownCategoryValues": "undefined:Games Console;Make:{0};".format(make["name"]),
            }

            request = Request(
                url="http://www.musicmagpie.co.uk/usercontrols/techService.asmx/GetModels",
                method='POST',
                body=json.dumps(formdata),
                headers={"Content-Type": "application/json; charset=UTF-8"},
                meta={"make": make["name"]},
                callback=self.parse_consoles_models,
            )

            yield request

    def parse_consoles_models(self, response):
        # Parsing JSON respones with models
        json_response = json.loads(response.body)

        for console in json_response["d"]:
            # For each model creating item
            item = GadgetScraperItem()
            item["make"] = response.meta["make"]
            item["model"] = console["name"]

            console_code = console["value"]

            # Creating request with according cookies
            # To get working piece price
            request = Request(
                url="http://www.musicmagpie.co.uk/start-selling/basket-condition",
                cookies={"musicMagpieVal": "loggedIn=0&barcode={0}&condition=5".format(console_code)},
                dont_filter=True,
                meta={"item": item, "console_code": console_code},
                callback=self.get_working_price,
            )

            yield request

    def get_working_price(self, response):
        # Removing null byte
        body = response.body.replace("\x00", "")
        response = response.replace(body=body)

        # Parsing working price
        item = response.meta["item"]
        item["working_price_1"] = response.xpath("//span[@class='blue strong']/text()").extract()[0]

        console_code = response.meta["console_code"]

        # And creating POST request with new cookie
        # To get poor piece price
        request = FormRequest(
            url="http://www.musicmagpie.co.uk/start-selling/basket-condition",
            formdata={
                "__EVENTTARGET": "ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition_11$ddlCondition",
                "ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition_11$ddlCondition": "6",
            },
            dont_filter=True,
            meta={"item": item},
            cookies={"musicMagpieVal": "loggedIn=0&barcode={0}&condition=6".format(console_code)},
            callback=self.get_broken_price,
        )

        yield request

    def get_broken_price(self, response):
        # Removing null byte
        body = response.body.replace("\x00", "")
        response = response.replace(body=body)

        # And parsing price
        item = response.meta["item"]
        item["broken_price_1"] = response.xpath("//span[@class='blue strong']/text()").extract()[0]

        yield item
