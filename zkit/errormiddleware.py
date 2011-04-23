#!/usr/bin/env python
#coding:utf-8
import sys
from cgi import escape
from traceback import format_exc

def ErrorMiddleware(application, render, template):
    def _(environ, start_response):
        try:
            application(environ, start_response)
        except:
            exc_info = sys.exc_info()

            traceback = format_exc()
            start_response(
                '500 Internal Server Error',
                [('content-type', 'text/html')],
                exc_info
            )
            return render(
                template,
                exc_info=exc_info,
                traceback=traceback,
                environ=environ
            )
            return [response]
    return _

