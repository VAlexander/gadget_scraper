#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os

sys.path.append(os.path.join(os.getcwd(), '../'))

import scrapy
from scrapy.crawler import CrawlerProcess
from spiders.compare_my_mobile_phones import CompareMyMobilePhonesSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(CompareMyMobilePhonesSpider)
process.start()