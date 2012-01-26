#coding:utf-8
import tornado.ioloop

class Run(object):
    def __init__(self, port, application):
        self.port = port
        self.application = application

    def __call__(self):
        import sys
        if len(sys.argv) > 1 and sys.argv[1].isdigit():
            port = int(sys.argv[1])
        else:
            port = self.port
            if type(port) in (list, tuple):
                port = port[0]

        print 'server on port %s'%port

        self.application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
