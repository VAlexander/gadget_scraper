#!/usr/bin/env python
#-*- coding:utf-8 -*-

## This script starts 6 spiders (phones, tablets, ipods, hand held consoles, consoles 
## and smartwatches) that should run monthly.
## When spiders complete scraping, they send .csv-formatted results to predefined address

import sys
import os

sys.path.append(os.path.join(os.getcwd(), '../'))

import scrapy
from scrapy.crawler import CrawlerProcess
from spiders.compare_my_mobile_ipods import CompareMyMobileIpodsSpider
from spiders.compare_my_mobile_handheld_consoles import CompareMyMobileHandheldConsolesSpider
from spiders.compare_my_mobile_consoles import CompareMyMobileConsolesSpider
from spiders.compare_my_mobile_smartwatches import CompareMyMobileSmartwatchesSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl(CompareMyMobileIpodsSpider)
process.crawl(CompareMyMobileHandheldConsolesSpider)
process.crawl(CompareMyMobileConsolesSpider)
process.crawl(CompareMyMobileSmartwatchesSpider)

process.start()
