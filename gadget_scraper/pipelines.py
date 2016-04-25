# -*- coding: utf-8 -*-

from datetime import datetime

from scrapy import signals
from scrapy.exporters import CsvItemExporter
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings

from product_mapping import Mapper


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
        file = open('scraping_result/{0}.csv'.format(spider.name), 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)

        if "compare_my_mobile" in spider.name:
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
        elif "music_magpie" in spider.name:
            self.exporter.fields_to_export = [
                "make",
                "model",
                "working_price_1",
                "poor_condition_price_1",
                "faulty_price_1",
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
        for field in item.keys():
            if "price" in field:
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
        self.mail_new_upload(spider)

    # Mailing result with attachments
    def mail_result(self, spider):
        settings = get_project_settings()

        mailer = MailSender.from_settings(settings)
        scrape_results_filename = 'scraping_result/{0}.csv'.format(spider.name)

        attachs = list()
        attachs.append((
            scrape_results_filename,
            'application/octet-stream',
            open(scrape_results_filename, "rb"),
        ))

        if spider.name in settings["SPIDER_MAPPING"]:
            mapping_details_filename = settings["SPIDER_MAPPING"][spider.name][0]
            zeroes_filename = settings["SPIDER_MAPPING"][spider.name][1]
            export_networks = settings["SPIDER_MAPPING"][spider.name][2]
            mapping_result_filename = 'mapping_result/ciyg_upload_{0}.csv'.format(spider.name)
            mapping_new_filename = 'mapping_result/ciyg_new_{0}.csv'.format(spider.name)

            m = Mapper(scrape_results_filename,
                       mapping_details_filename,
                       zeroes_filename,
                       mapping_result_filename,
                       mapping_new_filename,
                       export_networks)

            m.map_items()

            attachs.append((
                mapping_new_filename,
                'application/octet-stream',
                open(mapping_new_filename, "rb"),
            ))

        mailer.send(
            to=settings["MAIL_TO"],
            subject="Contents of scraping from {0} spider".format(spider.name),
            body="Contents of scraping from {0} spider\nDate of scrape: {1}".format(spider.name, datetime.now()),
            attachs=attachs
        )

    def mail_new_upload(self, spider):
        settings = get_project_settings()
        if spider.name in settings["SPIDER_MAPPING"]:
            mailer = MailSender.from_settings(settings)
            mapping_result_filename = 'mapping_result/ciyg_upload_{0}.csv'.format(spider.name)

            attachs = list()
            attachs.append((
                spider.upload_filename,
                'application/octet-stream',
                open(mapping_result_filename, "rb"),
            ))

            mailer.send(
                to=settings["MAIL_TO"],
                subject=spider.mapping_subject,
                body=spider.mapping_body.format(datetime.now()),
                attachs=attachs
            )
