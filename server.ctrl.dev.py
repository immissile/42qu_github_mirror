#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


from mylib import cookie_fix
from datetime import datetime
from os.path import join
from pprint import pformat
from mypy import mypyconfig
from myconf import config

#模板渲染的查找函数
mypyconfig.LOOKUP = config.MAKOLOOKUP

mypyconfig.FUNC_MODULE_PREFIX_LEN = len("mysite.ctrl.")


if config.THREAD_SAFE:
    import threading
    mypyconfig.LOCAL = threading.local()

from mypy.route_render import _ROUTE
from mypy.http_exc import Http404
from mypy import render
import mysite.ctrl
import mysite.ctrl.init_url
from mysite.ctrl.forward_middleware import forward_middleware
#初始化url route
_ROUTE._install(mysite.ctrl, "mysite.ctrl")


def application(request):
    render.LOCAL.request = request
    uri = request.uri
    try:
        try:
            result = _ROUTE << uri.path
        except Http404:
            from cgi import escape
            res = request.res
            user_agent = request.environ.get("HTTP_USER_AGENT")
            if not (user_agent and (' MSIE ' in user_agent or ' Chrome' in user_agent)):
                res.status = "404 Not Found"

            result = """<!doctype html>
<head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>%s 页面不存在</title></head>\
<body>\
<div style="text-align:center;padding:15px;font-size:16px;border:1px dashed #e0e0e0;line-height:30px;margin:10%% auto;width:39%%;font-family:Verdana">\
<p>网址有误 ?</p>\
<p>访问的页面不在这个宇宙</p>\
<p><a href="/" style="color:#01a">点击这里, 去其他地方逛逛 ...</a></p></div>\
</body>
"""%(escape(uri.path))
    except Exception:
        import traceback
        print >> sys.stderr, "\n\n"
        print >> sys.stderr, request.uri.path, datetime.now()
        print >> sys.stderr, ""
        print >> sys.stderr, pformat(dict([(k, v) for k, v in request.environ.iteritems() if k.isupper()]))
        print >> sys.stderr, ""
        traceback.print_exc()
        raise
    return str(result)

from mypy import profile_middleware
application = profile_middleware.ProfileMiddleware(application)


from mypy.gzip import GzipMiddleware
application = GzipMiddleware(application)

from mypy.yaro import Yaro, Response
application = Yaro(application)

ROOT_URL = _ROUTE._urlmap._urlmap.keys()
application = forward_middleware(application, ROOT_URL)

try:
    if config.DEBUG:
        from weberror.evalexception import EvalException
        application = EvalException(application, )
    else:
        from weberror.errormiddleware import ErrorMiddleware
        application = ErrorMiddleware(application, debug=True)
except ImportError:
    import traceback
    traceback.print_exc()

from mysite.model import init_db
profile_middleware.PROFILE_FUNC_LIST.append(init_db.mc)
profile_middleware.PROFILE_FUNC_LIST.append(init_db.SQLSTORE)


