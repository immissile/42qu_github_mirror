#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _url
from _urlmap import urlmap
import tornado.web
from config import SITE_URL, TWITTER_CONSUMER_SECRET, TWITTER_CONSUMER_KEY, GOOGLE_CONSUMER_SECRET, GOOGLE_CONSUMER_KEY

application = tornado.web.Application(
    tuple(urlmap.handlers),
    login_url='%s/auth/login' % SITE_URL,
    settings={
            'twitter_consumer_key':TWITTER_CONSUMER_KEY,
           'twitter_consumer_secret':TWITTER_CONSUMER_SECRET,
            'google_consumer_key': GOOGLE_CONSUMER_KEY,
            'google_consumer_secret':GOOGLE_CONSUMER_SECRET
        }
)
