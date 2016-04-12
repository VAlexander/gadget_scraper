# -*- coding: utf-8 -*-

from scrapy import Spider, Request, FormRequest
from scrapy.selector import Selector

try:
    from items import GadgetScraperItem
except ImportError:
    from gadget_scraper.items import GadgetScraperItem


class CompareMyMobileSmartwatchesSpider(Spider):
    name = "compare_my_mobile_smartwatches"
    allowed_domains = ["www.comparemymobile.com"]
    start_urls = ()

    device_div_xpath = "//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 text-center']"

    offer_xpath = "//div[@class='filter-result']"
    price_xpath = "string(.//span[@class='filter-price'])"

    def start_requests(self):
        ## Making requests
        requests = []

        requests.append(Request(
            url="http://www.comparemymobile.com/recycle/smart_watches/lg.html",
            meta={"make": "LG"},
            callback=self.parse_smartwatches_page,
        )
        )

        requests.append(Request(
            url="http://www.comparemymobile.com/recycle/smart_watches/samsung.html",
            meta={"make": "Samsung"},
            callback=self.parse_smartwatches_page,
        )
        )

        requests.append(Request(
            url="http://www.comparemymobile.com/recycle/smart_watches/sony.html",
            meta={"make": "Sony"},
            callback=self.parse_smartwatches_page,
        )
        )

        return requests

    def parse_smartwatches_page(self, response):
        ## Select every div for every single console
        for device_div in response.xpath(self.device_div_xpath):
            ## Set manufacturer from request's meta
            make = response.meta["make"]

            ## Get model from <a> text
            model = device_div.xpath("(.//a)[2]/text()").extract()[0]

            ## Create new item
            item = GadgetScraperItem()
            item["make"] = make
            item["model"] = model.strip()

            ## Get URL for price comparsion
            url = device_div.xpath("(.//a)[2]/@href").extract()[0]
            ## Set item to meta
            meta = {"item": item}

            ## And yield the request to get working prices
            yield Request(url=url, meta=meta, callback=self.get_working_prices)

    def get_device_id(self, response):
        ## Get device's ID for AJAX requests via RegExp
        selector = Selector(response=response)
        device_id = selector.re(r"var device_id = '(\d+)';")[0]

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
