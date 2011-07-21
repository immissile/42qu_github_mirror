#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _url
from _urlmap import urlmap
import tornado.web
from config import SITE_URL, TWITTER_CONSUMER_SECRET, TWITTER_CONSUMER_KEY

application = tornado.web.Application(
    tuple(urlmap.handlers),
    login_url='%s/auth/login' % SITE_URL,
    settings={
            'twitter_consumer_key':TWITTER_CONSUMER_KEY,
            'twitter_consumer_secret':TWITTER_CONSUMER_SECRET,
        }
)
