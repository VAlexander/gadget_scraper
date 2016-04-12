#!/usr/bin/env python
#-*- coding:utf-8 -*-

## This script starts 2 spiders (for phones and for tablets) that should run daily
## When spiders complete scraping, they send .csv-formatted results to predefined address

import sys
import os

sys.path.append(os.path.join(os.getcwd(), '../'))

import scrapy
from scrapy.crawler import CrawlerProcess
from spiders.compare_my_mobile_phones import CompareMyMobilePhonesSpider
from spiders.compare_my_mobile_tablets import CompareMyMobileTabletsSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl(CompareMyMobilePhonesSpider)
process.crawl(CompareMyMobileTabletsSpider)
process.start()
