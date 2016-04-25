#!/usr/bin/env python
# -*- coding:utf-8 -*-

# This script starts spiders for consoles category at musicmagpie.co.uk
# When spider completes scraping, it sends .csv-formatted results to predefined address

import os
import sys

sys.path.append(os.path.join(os.getcwd(), '../'))

from scrapy.crawler import CrawlerProcess
from spiders.music_magpie_ipods import MusicMagpieIpodsSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(MusicMagpieIpodsSpider)
process.start()
