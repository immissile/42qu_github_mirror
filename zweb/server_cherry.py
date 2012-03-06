#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from cherrypy.wsgiserver import CherryPyWSGIServer
from time import time


def timeit_middleware(func):
    def _(environ, start_response):
        begin = time()
        result = func(environ, start_response)
        logging.info(
            '\n%.2f\t%s //%s%s\n\n------------------------------------------'%(
                    (1000*(time() - begin)),
                    environ.get('REQUEST_METHOD'),
                    environ.get('HTTP_HOST'),
                    environ.get('PATH_INFO'),
            )
        )
        return result
    return _

def WSGIServer(port, application):
    from weberror.evalexception import EvalException
    application = EvalException(application, )
    application = timeit_middleware(application)
    logging.info('\nGAME BEGIN\n\n')
    
    server = CherryPyWSGIServer(('0.0.0.0', port), application, numthreads=10)

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


