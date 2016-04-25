# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest
from scrapy.selector import Selector

try:
    from items import GadgetScraperItem
except ImportError:
    from gadget_scraper.items import CompareMyMobileItem
import json


class CompareMyMobileTabletsSpider(Spider):
    ## This spider scrapes comparemymobile.com website for tablets

    ## Apple, Acer, Advent, Alcatel, Asus, BlackBerry,
    ## Dell, ExoPC, Google, HTC, Huawei, LG, Microsoft, Motorola, Nokia,
    ## Samsung, Sony and Amazon Kindle

    name = "compare_my_mobile_tablets"
    allowed_domains = ["comparemymobile.com"]
    start_urls = ()

    upload_filename = 'Tablet update.csv'
    mapping_subject = 'Mapping for tablets'
    mapping_body = "Mapping for tablets\nDate of mapping: {0}"

    tablet_div_xpath = "//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 text-center']"
    galaxy_tab_div_xpath = "//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2']"

    offer_xpath = "//div[@class='filter-result']"
    price_xpath = "string(.//span[@class='filter-price'])"

    def start_requests(self):
        ## Making requests
        requests = []

        ## Apple, complicated chain of functions
        requests.append(Request(
        url="http://www.comparemymobile.com/sell/ipad",
        meta={"make": "Apple"},
        callback=self.get_ipad_type,
        )
        )

        ## Kindle, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/sell/kindle",
        meta={"make": "Amazon"},
        callback=self.parse_tablets_page,
        )
        )

        ## Acer, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/acer.html",
        meta={"make": "Acer"},
        callback=self.parse_tablets_page,
        )
        )

        ## Advent, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/advent.html",
        meta={"make": "Advent"},
        callback=self.parse_tablets_page,
        )
        )

        ## Alcatel, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/alcatel.html",
        meta={"make": "Alcatel"},
        callback=self.parse_tablets_page,
        )
        )

        ## Asus, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/asus.html",
        meta={"make": "Asus"},
        callback=self.parse_tablets_page,
        )
        )

        ## BlackBerry, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/sell/blackberry-playbook",
        meta={"make": "BlackBerry"},
        callback=self.parse_tablets_page,
        )
        )

        ## Dell, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/dell.html",
        meta={"make": "Dell"},
        callback=self.parse_tablets_page,
        )
        )

        ## ExoPC, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/exopc.html",
        meta={"make": "ExoPC"},
        callback=self.parse_tablets_page,
        )
        )

        ## Google, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/google.html",
        meta={"make": "Google"},
        callback=self.parse_tablets_page,
        )
        )

        ## HTC, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/htc.html",
        meta={"make": "HTC"},
        callback=self.parse_tablets_page,
        )
        )

        ## Huawei, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/huawei.html",
        meta={"make": "Huawei"},
        callback=self.parse_tablets_page,
        )
        )

        ## LG, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/lg.html",
        meta={"make": "LG"},
        callback=self.parse_tablets_page,
        )
        )

        ## Microsoft, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/sell/microsoft-surface-tablets",
        meta={"make": "Microsoft"},
        callback=self.parse_tablets_page,
        )
        )

        ## Motorola, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/sell/motorola-xoom-tablets",
        meta={"make": "Motorola"},
        callback=self.parse_tablets_page,
        )
        )

        ## Nokia, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/sell/nokia-lumia-tablets",
        meta={"make": "Nokia"},
        callback=self.parse_tablets_page,
        )
        )

        ## Samsung, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/samsung.html",
        meta={"make": "Samsung"},
        callback=self.parse_tablets_page,
        )
        )

        ## Galaxy Tab, separate request
        requests.append(Request(
            url="http://www.comparemymobile.com/sell/samsung-galaxy-tab",
            meta={"make": "Samsung"},
            callback=self.parse_galaxy_tab_page,
        )
        )

        ## Sony, every product is on page
        requests.append(Request(
        url="http://www.comparemymobile.com/recycle/tablets/sony.html",
        meta={"make": "Sony"},
        callback=self.parse_tablets_page,
        )
        )

        ## And returning them as initial
        return requests

    def parse_tablets_page(self, response):
        ## Select every div for every single tablet
        for tablet_div in response.xpath(self.tablet_div_xpath):
            ## Set manufacturer from request's meta
            make = response.meta["make"]

            ## Get model from <a> text
            model = tablet_div.xpath("(.//a)[2]/text()").extract()[0]

            ## Create new item
            item = CompareMyMobileItem()
            item["make"] = make
            item["model"] = model.strip()

            ## Get URL for price comparsion
            url = tablet_div.xpath("(.//a)[2]/@href").extract()[0]
            ## Set item to meta
            meta = {"item": item}

            ## And yield the request to get working prices
            yield Request(url=url, meta=meta, callback=self.get_working_prices)

    def parse_galaxy_tab_page(self, response):
        ## Select every div for every single tablet
        for galaxy_tab_div in response.xpath(self.galaxy_tab_div_xpath):
            url = galaxy_tab_div.xpath("./a/@href").extract()[0]
            url = "http://www.comparemymobile.com" + url
            meta = response.meta

            ## And yield the request to get working prices
            yield Request(url=url, meta=meta, callback=self.parse_tablets_page)

    def get_device_id(self, response):
        ## Get device's ID for AJAX requests via RegExp
        selector = Selector(response=response)
        try:
            device_id = selector.re(r"var device_id = '(\d+)';")[0]
        except IndexError:
            return False

        return device_id

    def get_working_prices(self, response):
        ## Get prices for working pieces via HTTP
        good_prices = []

        ## Scrape them all
        for offer in response.xpath(self.offer_xpath):
            price = offer.xpath(self.price_xpath).extract()[0]
            good_prices.append(price)

        item_fields = [
            "working_price_1",
            "working_price_2",
            "working_price_3",
            "working_price_4",
            "working_price_5",
            "working_price_6"]
        item = response.meta["item"]

        ## And populate item's fields
        for field, value in zip(item_fields, good_prices):
            item[field] = value

        ## Get device's ID
        device_id = self.get_device_id(response)

        ## If failed, then nothing to do here
        if not device_id:
            return

        ## Set data for AJAX request
        url = "http://www.comparemymobile.com/ajax-data"
        meta = {"item": item}
        formdata = {
            "task": "get_prices",
            "network": "0",
            "condition": "2",
            "device_id": device_id,
        }

        ## And yield it
        yield FormRequest(url=url, formdata=formdata, meta=meta, callback=self.get_broken_prices)

    def get_broken_prices(self, response):
        ## Get prices for broken pieces via AJAX
        broken_prices = []

        ## Scrape them all
        for div in response.xpath(self.offer_xpath):
            price = div.xpath(self.price_xpath).extract()[0]
            broken_prices.append(price)

        item_fields = [
            "broken_price_1",
            "broken_price_2",
            "broken_price_3",
            "broken_price_4",
            "broken_price_5",
            "broken_price_6"]
        item = response.meta["item"]

        ## And populate item's fields
        for field, value in zip(item_fields, broken_prices):
            item[field] = value

        yield item

    ## Select iPad type
    def get_ipad_type(self, response):
        for stage_1_link in response.xpath("//div[@class='stage1']/ul/li/a/@data-group0").extract():
            yield FormRequest(
                url="http://www.comparemymobile.com/ajax-data",
                formdata={
                    "task": "group0",
                    "manufacturer": "159",
                    "category": "7",
                    "group": stage_1_link
                },
                callback=self.get_ipad_model
            )

    ## Select iPad model
    def get_ipad_model(self, response):
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
                callback=self.get_ipad_storage_size
            )

    ## Select storage size
    def get_ipad_storage_size(self, response):
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
                callback=self.get_ipad_connectivity
            )

    ## Select connectivity type
    def get_ipad_connectivity(self, response):
        j = json.loads(response.body)
        for i in j["items"]:
            item = CompareMyMobileItem()
            item["make"] = "Apple"
            item["model"] = "{0} {1} {2}".format(i["group1"], i["group2"], i["group3"])

            meta = {"item": item}

            yield Request(url=i["url"], meta=meta, callback=self.get_working_prices)
