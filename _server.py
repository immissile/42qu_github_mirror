import config
import tornado.ioloop

class Run(object):
    def __init__(self, port):
        self.port = port

    def __call__(self):
        from god._application import application
        import sys
        if len(sys.argv) > 1 and sys.argv[1].isdigit():
            port = int(sys.argv[1])
        else:
            port = self.port
            if type(port) in (list, tuple):
                port = port[0]
        print 'server on port %s'%port

        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
