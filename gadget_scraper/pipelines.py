# -*- coding: utf-8 -*-

from datetime import datetime

from scrapy.exporters import CsvItemExporter
from scrapy.mail import MailSender
from scrapy import signals
from scrapy.utils.project import get_project_settings


class GadgetScraperPipeline(object):
    # Initialize files
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    # When spider opened, prepare csv exporter
    def spider_opened(self, spider):
        file = open('{0}.csv'.format(spider.name), 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = [
            "make",
            "model",
            "working_price_1",
            "working_price_2",
            "working_price_3",
            "working_price_4",
            "working_price_5",
            "working_price_6",
            "broken_price_1",
            "broken_price_2",
            "broken_price_3",
            "broken_price_4",
            "broken_price_5",
            "broken_price_6",
        ]
        self.exporter.encoding = "utf-8"
        self.exporter.start_exporting()

    # Processing each item
    def process_item(self, item, spider):
        item = self.remove_pound_symbol(item)
        self.exporter.export_item(item)
        return item

    # Removing trailing English pound symbol
    def remove_pound_symbol(self, item):
        price_fields = [
            "working_price_1",
            "working_price_2",
            "working_price_3",
            "working_price_4",
            "working_price_5",
            "working_price_6",
            "broken_price_1",
            "broken_price_2",
            "broken_price_3",
            "broken_price_4",
            "broken_price_5",
            "broken_price_6"
        ]

        for field in price_fields:
            try:
                # If we got pound symbol
                if not item[field][0].isdigit():
                    # Remove it and strip the data
                    item[field] = item[field][1:].strip()
            except KeyError:
                item[field] = "0"
            except IndexError:
                pass

        return item

    # When spider closed, finish exporting and close the file
    # After that, mail the result
    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

        self.mail_result(spider)

    # Mailing result with attachments
    def mail_result(self, spider):
        settings = get_project_settings()

        mailer = MailSender.from_settings(settings)
        filename = '{0}.csv'.format(spider.name)
        mailer.send(
            to=settings["MAIL_TO"],
            subject="Contents of scraping from {0} spider".format(spider.name),
            body="Contents of scraping from {0} spider\nDate of scrape: {1}".format(spider.name, datetime.now()),
            attachs=[(
                filename,
                'application/octet-stream',
                open(filename, "rb"),
            )]
        )
