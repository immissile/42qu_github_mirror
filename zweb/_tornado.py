#!/usr/bin/env python
#coding:utf-8


from tornado import web
from tornado.web import HTTPError
from config import SITE_DOMAIN_SUFFIX

_set_cookie = web.RequestHandler.set_cookie

def set_cookie(
    self, name, value, domain=SITE_DOMAIN_SUFFIX, expires=None, path="/",
    expires_days=None, **kwargs
):
    _set_cookie(
        self,
        name, value, domain, expires,
        path, expires_days, **kwargs
    )

web.RequestHandler.set_cookie = set_cookie


def _execute(self, transforms, *args, **kwargs):
    """Executes this request with the given output transforms."""
    self._transforms = transforms
    if self.request.method not in self.SUPPORTED_METHODS:
        raise HTTPError(405)
    # If XSRF cookies are turned on, reject form submissions without
    # the proper cookie
    if self.request.method not in ("GET", "HEAD") and \
       self.application.settings.get("xsrf_cookies"):
        self.check_xsrf_cookie()
    self.prepare()
    if not self._finished:
        getattr(self, self.request.method.lower())(*args, **kwargs)
        if self._auto_finish and not self._finished:
            self.finish()
web.RequestHandler._execute = _execute



def redirect(self, url, permanent=False):
    """Sends a redirect to the given (optionally relative) URL."""
    if self._headers_written:
        raise Exception("Cannot redirect after headers have been written")
    self.set_status(301 if permanent else 302)
    self.set_header("Location", url)
    self.finish()

web.RequestHandler.redirect = redirect

def xsrf_form_html(self):
    return '<input type="hidden" name="_xsrf" value="%s">'%self.xsrf_token

web.RequestHandler.xsrf_form_html = xsrf_form_html
