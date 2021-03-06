#!/usr/bin/env python
# -*- coding:utf-8 -*-

# This script starts spider for handheld consoles category at www.comparemymobile.com
# When spider completes scraping, it sends .csv-formatted results to predefined address

import os
import sys

sys.path.append(os.path.join(os.getcwd(), '../'))

from scrapy.crawler import CrawlerProcess
from spiders.compare_my_mobile_handheld_consoles import CompareMyMobileHandheldConsolesSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(CompareMyMobileHandheldConsolesSpider)
process.start()
