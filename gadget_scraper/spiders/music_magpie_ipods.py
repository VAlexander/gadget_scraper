# -*- coding: utf-8 -*-

import json

from scrapy import Spider, Request, FormRequest

try:
    from items import MusicMagpieItem
except ImportError:
    from gadget_scraper.items import MusicMagpieItem


class MusicMagpieIpodsSpider(Spider):
    name = "music_magpie_ipods"
    allowed_domains = ["musicmagpie.co.uk"]
    start_urls = ("http://www.musicmagpie.co.uk/",)

    def parse(self, response):
        # Creating request to get all the iPods numbers
        # via JSON POST request
        formdata = {
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
        # Parsing JSON response
        json_response = json.loads(response.body)

        # And creating item and request for each iPod entry
        for ipod_entry in json_response["d"]:
            item = MusicMagpieItem()
            model = ipod_entry["name"].strip()

            item["make"] = response.meta["make"]
            item["model"] = model

            ipod_code = ipod_entry["value"]

            # Creating request with according cookies
            # To get working piece price
            request = Request(
                url="http://www.musicmagpie.co.uk/start-selling/basket-condition",
                cookies={"musicMagpieVal": "loggedIn=0&barcode={0}&condition=5".format(ipod_code)},
                dont_filter=True,
                meta={"item": item, "ipod_code": ipod_code},
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

        ipod_code = response.meta["ipod_code"]

        # And creating POST request with new cookie
        # To get poor piece price
        request = FormRequest(
            url="http://www.musicmagpie.co.uk/start-selling/basket-condition",
            formdata={
                "__EVENTTARGET": "ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition_11$ddlCondition",
                "ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition_11$ddlCondition": "6",
            },
            dont_filter=True,
            meta={"item": item, "ipod_code": ipod_code},
            cookies={"musicMagpieVal": "loggedIn=0&barcode={0}&condition=6".format(ipod_code)},
            callback=self.get_poor_price,
        )

        yield request

    def get_poor_price(self, response):
        # Removing null byte
        body = response.body.replace("\x00", "")
        response = response.replace(body=body)

        # And parsing price
        item = response.meta["item"]
        item["poor_condition_price_1"] = response.xpath("//span[@class='blue strong']/text()").extract()[0]

        ipod_code = response.meta["ipod_code"]

        # And creating POST request with new cookie
        # To get faulty piece price
        request = FormRequest(
            url="http://www.musicmagpie.co.uk/start-selling/basket-condition",
            formdata={
                "__EVENTTARGET": "ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition_11$ddlCondition",
                "ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$itemCondition_11$ddlCondition": "7",
            },
            dont_filter=True,
            meta={"item": item, "ipod_code": ipod_code},
            cookies={"musicMagpieVal": "loggedIn=0&barcode={0}&condition=7".format(ipod_code)},
            callback=self.get_faulty_price,
        )

        yield request

    def get_faulty_price(self, response):
        # Removing null byte
        body = response.body.replace("\x00", "")
        response = response.replace(body=body)

        # And parsing price
        item = response.meta["item"]
        item["faulty_price_1"] = response.xpath("//span[@class='blue strong']/text()").extract()[0]

        yield item