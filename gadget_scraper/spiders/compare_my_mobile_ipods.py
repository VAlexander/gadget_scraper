# -*- coding: utf-8 -*-

from scrapy import Spider, Request, FormRequest
from scrapy.selector import Selector

try:
    from items import GadgetScraperItem
except ImportError:
    from gadget_scraper.items import CompareMyMobileItem


class CompareMyMobileIpodsSpider(Spider):
    name = "compare_my_mobile_ipods"
    allowed_domains = ["www.comparemymobile.com"]
    start_urls = ()

    ipod_div_xpath = "//div[@class='col-xs-6 col-sm-3 col-md-2 col-lg-2']"
    ipod_model_div_xpath = "./div[@class='text-center h4']/text()"

    offer_xpath = "//div[@class='filter-result']"
    price_xpath = "string(.//span[@class='filter-price'])"

    ipod_urls = [
        "http://www.comparemymobile.com/sell/ipod-touch",
        "http://www.comparemymobile.com/sell/ipod-classic",
        "http://www.comparemymobile.com/sell/ipod-nano",
        "http://www.comparemymobile.com/sell/ipod-shuffle"
    ]

    def start_requests(self):
        ## Making requests
        requests = []

        for ipod_url in self.ipod_urls:
            requests.append(Request(
                url=ipod_url,
                callback=self.parse_ipods_page,
            )
            )

        return requests

    def parse_ipods_page(self, response):
        ## Get every div for iPhone
        for ipod_div in response.xpath(self.ipod_div_xpath):
            ## Set manufacturer
            make = "Apple"
            ## And get model (for example, iPod Touch 5th Gen)
            model = ipod_div.xpath(self.ipod_model_div_xpath).extract()[0]

            ## Then, get all the options for current model
            capacity_divs = ipod_div.xpath(".//a")
            for capacity_div in capacity_divs:
                ## For every option, scrape its data
                ## For example, "16GB prices" becomes just "16GB"
                capacity = capacity_div.xpath("./text()").extract()[0].split(" ")[0]

                ## Create new item and set data for it
                item = CompareMyMobileItem()
                item["make"] = make
                item["model"] = "{0} {1}".format(model, capacity)

                ## Prepare data for HTML request
                url = capacity_div.xpath("./@href").extract()[0]
                meta = {"item": item}

                ## And yield it
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
