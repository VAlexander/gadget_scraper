#!/usr/bin/env python
#-*- coding:utf-8 -*-

## This script starts musicmagpie.co.uk spiders for ipods and consoles
## When spiders complete scraping, they send .csv-formatted results to predefined address

import sys
import os

sys.path.append(os.path.join(os.getcwd(), '../'))

import scrapy
from scrapy.crawler import CrawlerProcess
from spiders.music_magpie_consoles import MusicMagpieConsolesSpider
from spiders.music_magpie_ipods import MusicMagpieIpodsSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl(MusicMagpieConsolesSpider)
process.crawl(MusicMagpieIpodsSpider)
process.start()
