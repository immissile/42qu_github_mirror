#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cherrypy.wsgiserver import CherryPyWSGIServer

def WSGIServer(port, application):
    from weberror.evalexception import EvalException
    application = EvalException(application, )
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        datefmt='%H:%M:%S',
    )
    def _(environ, start_response):
        logging.info('%s %s'%(environ.get('REQUEST_METHOD'), environ.get('PATH_INFO')))
        return application(environ, start_response)
    return CherryPyWSGIServer(('0.0.0.0', port), _, numthreads=10)
