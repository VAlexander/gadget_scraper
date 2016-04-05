# -*- coding: utf-8 -*-

import os
import random
from scrapy.conf import settings

class RandomUserAgentMiddleware(object):
	def process_request(self, request, spider):
		user_agent	= random.choice(settings.get('USER_AGENT_LIST'))
		if user_agent:
			request.headers.setdefault('User-Agent', user_agent)

class ProxyMiddleware(object):
	def process_request(self, request, spider):
		request.meta['proxy'] = settings.get('HTTP_PROXY')