#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zpage_host
SITE_DOMAIN = "42qu.info"
zpage_host.SITE_DOMAIN = SITE_DOMAIN
zpage_host.SITE_URL = "http://%s"%SITE_DOMAIN
zpage_host.SITE_DOMAIN_SUFFIX = ".%s"%(SITE_DOMAIN)
