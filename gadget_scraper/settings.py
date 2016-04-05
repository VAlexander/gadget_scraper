# -*- coding: utf-8 -*-

## Email configuration
MAIL_TO = ['']
MAIL_FROM = 'root@localhost'
MAIL_HOST = 'localhost'
MAIL_PORT = 25

## Concurrent requests for the domain (4 is enough)
CONCURRENT_REQUESTS=4

## Delay between requests so we won't DoS other server
## Somewhere between 1 and 2 is OK
DOWNLOAD_DELAY=2


######################################################
## Spiders' internals, no need to modify them		##
######################################################

LOG_LEVEL = "DEBUG"

BOT_NAME = 'gadget_scraper'

SPIDER_MODULES = ['gadget_scraper.spiders']
NEWSPIDER_MODULE = 'gadget_scraper.spiders'

ITEM_PIPELINES = {
	'gadget_scraper.pipelines.GadgetScraperPipeline': 300,
}

USER_AGENT_LIST = [
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 \
		 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
	'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) \
	   Gecko/16.0 Firefox/16.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 \
	   (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
]

HTTP_PROXY = 'http://127.0.0.1:9050'

DOWNLOADER_MIDDLEWARES = {
	 'gadget_scraper.middlewares.RandomUserAgentMiddleware': 400,
	 'gadget_scraper.middlewares.ProxyMiddleware': 410,
	 'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None
	# Disable compression middleware, so the actual HTML pages are cached
}