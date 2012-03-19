#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Cookie
import base64
import calendar
import datetime
import email.utils
import functools
import gzip
import hashlib
import hmac
import httplib
import logging
import mimetypes
import os.path
import re
import stat
import sys
import time
import types
import urllib
import urlparse
import uuid

from tornado import web
from tornado.web import HTTPError, utf8
from zkit.tld_name import tld_name
from profile_middleware import profile_middleware

from tornado import escape
from tornado import locale
from tornado import stack_context
from tornado import template

def set_cookie(self, name, value, domain=None, expires=None, path='/',
               expires_days=None, **kwargs):
    """Sets the given cookie name/value with the given options.

    Additional keyword arguments are set on the Cookie.Morsel
    directly.
    See http://docs.python.org/library/cookie.html#morsel-objects
    for available attributes.
    """
    if domain is None:
        domain = '.%s'%tld_name(self.request.host)
    name = utf8(name)
    value = utf8(value)
    if re.search(r"[\x00-\x20]", name + value):
        # Don't let us accidentally inject bad stuff
        raise ValueError('Invalid cookie %r: %r' % (name, value))
    if not hasattr(self, '_new_cookies'):
        self._new_cookies = []
    new_cookie = Cookie.BaseCookie()
    self._new_cookies.append(new_cookie)
    new_cookie[name] = value
    if domain:
        new_cookie[name]['domain'] = domain

    if expires_days is not None and not expires:
        expires = datetime.datetime.utcnow() + datetime.timedelta(
            days=expires_days)
    if expires:
        if type(expires) is not str:
            timestamp = calendar.timegm(expires.utctimetuple())
            expires = email.utils.formatdate(
                timestamp, localtime=False, usegmt=True
            )
        new_cookie[name]['expires'] = expires
    else:
        new_cookie[name]['expires'] = 'Tue, 01 Jan 2030 00:00:00 GMT'

    if path:
        new_cookie[name]['path'] = path
    for k, v in kwargs.iteritems():
        new_cookie[name][k] = v

web.RequestHandler.set_cookie = set_cookie


def clear_cookie(self, name, path='/', domain=None):
    """Deletes the cookie with the given name."""
    expires = 'Tue, 01 Jun 2000 00:00:00 GMT'
    self.set_cookie(name, value='', path=path, expires=expires, domain=domain)

web.RequestHandler.clear_cookie = clear_cookie


from model._db import SQLSTORE, mc
from os import getpid

PID = str(getpid()).ljust(7)

#logging.warn("PID:%s", PID)

@profile_middleware([SQLSTORE, mc])
def _execute(self, transforms, *args, **kwargs):
    """Executes this request with the given output transforms."""
    request = self.request
    method = request.method
    self._transforms = transforms

    if method not in self.SUPPORTED_METHODS:
        raise HTTPError(405)

#    logging.warn("PID %s %s %s %s%s", PID, self.get_cookie('S') or '-', method, request.host, request.path,)

    if method not in ('GET', 'HEAD') and self.application.settings.get('xsrf_cookies'):
        self.check_xsrf_cookie()
    self.prepare()
    if not self._finished:
        getattr(self, method.lower())(*args, **kwargs)
        if self._auto_finish and not self._finished:
            self.finish()

    #logging.warn("END %s %s%s", PID, request.host, request.path)

web.RequestHandler._execute = _execute


def redirect(self, url, permanent=False):
    """Sends a redirect to the given (optionally relative) URL."""
    if self._headers_written:
        raise Exception('Cannot redirect after headers have been written')
    self.set_status(301 if permanent else 302)
    self.set_header('Location', url)
    self.finish()

web.RequestHandler.redirect = redirect


def xsrf_form_html(self):
    return '<input type="hidden" name="_xsrf" value="%s">'%self.xsrf_token

web.RequestHandler.xsrf_form_html = xsrf_form_html

