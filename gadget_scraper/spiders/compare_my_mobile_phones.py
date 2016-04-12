# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest
from scrapy.selector import Selector

try:
    from items import GadgetScraperItem
except ImportError:
    from gadget_scraper.items import GadgetScraperItem


class CompareMyMobilePhonesSpider(Spider):
    # This spider scrapes comparemymobile.com website for phones
    # Apple, Samsung, Sony, HTC, Nokia, LG and Blackberry handsets

    name = "compare_my_mobile_phones"
    allowed_domains = ["comparemymobile.com"]
    start_urls = ()

    iphone_div_xpath = "//div[@class='col-xs-6 col-sm-3 col-md-2 col-lg-2']"
    iphone_model_div_xpath = "./div[@class='text-center h4']/text()"

    phone_div_xpath = "//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 text-center']"

    galaxy_s_div_xpath = "//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2']"

    offer_xpath = "//div[@class='filter-result']"
    price_xpath = "string(.//span[@class='filter-price'])"

    def start_requests(self):
        # Making requests to scrape all phones
        requests = []

        # Request for iPhones (unique, that's why separated function used)
        requests.append(Request(
            url="http://www.comparemymobile.com/sell/iphone",
            callback=self.parse_iphones_page,
        )
        )

        # Samsung, #199
        requests.append(FormRequest(
            url="http://www.comparemymobile.com/ajax-data",
            formdata={
                "task": "full_phone_list",
                "m": "199",
                "cat": "1",
            },
            meta={"make": "Samsung"},
            callback=self.parse_phones_page
        )
        )

        # Samsung Galaxy S, separate request
        requests.append(Request(
            url="http://www.comparemymobile.com/sell/samsung-galaxy-s",
            callback=self.parse_galaxy_s_page,
        )
        )

        # Sony, all phones shown during initial request
        requests.append(Request(
            url="http://www.comparemymobile.com/recycle/sony.html",
            meta={"make": "Sony"},
            callback=self.parse_phones_page,
        )
        )

        # HTC, #176
        requests.append(FormRequest(
            url="http://www.comparemymobile.com/ajax-data",
            formdata={
                "task": "full_phone_list",
                "m": "176",
                "cat": "1",
            },
            meta={"make": "HTC"},
            callback=self.parse_phones_page
        )
        )

        # Nokia, #191
        requests.append(FormRequest(
            url="http://www.comparemymobile.com/ajax-data",
            formdata={
                "task": "full_phone_list",
                "m": "191",
                "cat": "1",
            },
            meta={"make": "Nokia"},
            callback=self.parse_phones_page
        )
        )

        # LG, #183
        requests.append(FormRequest(
            url="http://www.comparemymobile.com/ajax-data",
            formdata={
                "task": "full_phone_list",
                "m": "183",
                "cat": "1",
            },
            meta={"make": "LG"},
            callback=self.parse_phones_page
        )
        )

        # BlackBerry, #166
        requests.append(FormRequest(
            url="http://www.comparemymobile.com/ajax-data",
            formdata={
                "task": "full_phone_list",
                "m": "166",
                "cat": "1",
            },
            meta={"make": "BlackBerry"},
            callback=self.parse_phones_page
        )
        )

        # And returning it as initial
        return requests

    def parse_phones_page(self, response):
        # Select every div for every single phone
        for phone_div in response.xpath(self.phone_div_xpath):
            # Set manufacturer from request's meta
            make = response.meta["make"]

            # Get model from <a> text
            model = phone_div.xpath("(.//a)[2]/text()").extract()[0]

            # Create new item
            item = GadgetScraperItem()
            item["make"] = make
            item["model"] = model.strip()

            # Get URL for price comparsion
            url = phone_div.xpath("(.//a)[2]/@href").extract()[0]
            # Set item to meta
            meta = {"item": item}

            # And yield the request to get working prices
            yield Request(url=url, meta=meta, callback=self.get_working_prices)

    def parse_iphones_page(self, response):
        # Get every div for iPhone
        for div in response.xpath(self.iphone_div_xpath):
            # Set manufacturer
            make = "Apple"
            # And get model (for example, iPhone 6s Plus)
            model = div.xpath(self.iphone_model_div_xpath).extract()[0]

            # Then, get all the options for current model
            buttons = div.xpath(".//a")
            for button in buttons:
                # For every option, scrape its data
                # For example, "16GB prices" becomes just "16GB"
                capacity = button.xpath("./text()").extract()[0].split(" ")[0]

                # Create new item and set data for it
                item = GadgetScraperItem()
                item["make"] = make
                item["model"] = "{0} {1}".format(model, capacity)

                # Prepare data for HTML request
                url = button.xpath("./@href").extract()[0]
                meta = {"item": item}

                # And yield it
                yield Request(url=url, meta=meta, callback=self.get_working_prices)

    def parse_galaxy_s_page(self, response):
        # Get every div for Samsung Galaxy S phone
        for galaxy_s_div in response.xpath(self.galaxy_s_div_xpath):

            # And get model (for example, Galaxy S6 Edge)
            model = galaxy_s_div.xpath("./div[@class='text-center h4']/text()").extract()[0]

            # Then, get all the options for current model
            for button in galaxy_s_div.xpath(".//a"):
                # Get submodel and delete 'prices'. 
                # For example, 'Galaxy S i9000 prices' becomes 'Galaxy S i9000'
                submodel = button.xpath("./text()").extract()[0]
                submodel = submodel.replace(" prices", "")

                # Create new item and set data for it
                item = GadgetScraperItem()
                item["make"] = "Samsung"

                if model != submodel:
                    item["model"] = "{0} {1}".format(model, submodel)
                else:
                    item["model"] = "{0}".format(model)

                # Prepare data for HTML request
                url = button.xpath("./@href").extract()[0]
                meta = {"item": item}

                # And yield it
                yield Request(url=url, meta=meta, callback=self.get_working_prices)

    def get_device_id(self, response):
        # Get device's ID for AJAX requests via RegExp
        selector = Selector(response=response)
        device_id = selector.re(r"var device_id = '(\d+)';")[0]

        return device_id

    def get_working_prices(self, response):
        # Get prices for working pieces via HTTP
        good_prices = []

        # Scrape them all
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

        # And populate item's fields
        for field, value in zip(item_fields, good_prices):
            item[field] = value

        # Get device's ID
        device_id = self.get_device_id(response)

        # Set data for AJAX request
        url = "http://www.comparemymobile.com/ajax-data"
        meta = {"item": item}
        formdata = {
            "task": "get_prices",
            "network": "0",
            "condition": "2",
            "device_id": device_id,
        }

        # And yield it
        yield FormRequest(url=url, formdata=formdata, meta=meta, callback=self.get_broken_prices)

    def get_broken_prices(self, response):
        # Get prices for broken pieces via AJAX
        broken_prices = []

        # Scrape them all
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

        # And populate item's fields
        for field, value in zip(item_fields, broken_prices):
            item[field] = value

        yield item
