import beanstalkc
from _db import cursor_by_table
from marshal import dumps, loads
from decorator import decorator
from config import MQ_PORT, MQ_USE
import logging
from config import DEBUG

beanstalk = None
NAME2FUNC = {}

if DEBUG:
    def mq_client(func, name=None):
        return func
else:
    def mq_client(func, name=None):
        name = name or func.__name__
        NAME2FUNC[name] = func
        def _func(func, *args, **kwds):
            global beanstalk
            if beanstalk is None:
                beanstalk = beanstalkc.Connection(host='localhost', port=MQ_PORT, parse_yaml=True)
                beanstalk.use(MQ_USE)
            #print (name, args, kwds)
            s = dumps((name, args, kwds))
            beanstalk.put(s)
        return decorator(_func, func)

def mq_server():
    print 'mq_server on port %s' % MQ_PORT
    beanstalk = beanstalkc.Connection(
        host='localhost',
        port=MQ_PORT,
        parse_yaml=True
    )
    beanstalk.watch(MQ_USE)
    beanstalk.ignore('default')
    while True:
        job = beanstalk.reserve()
        #print job
        try:
            name, args, kwds = loads(job.body)
        except:
            job.delete()
            continue

        func = NAME2FUNC.get(name)
        #print name, args, kwds

        try:
            func(*args, **kwds)
        except:
            import traceback
            exc = traceback.format_exc()
            cursor = cursor_by_table('failed_mq')
            cursor.execute('insert into failed_mq (body,exc,func) values (%s,%s,%s)', (job.body, exc, name))
            logging.error(exc)
        job.delete()


def mq_clear(func):
    job = beanstalk.reserve(0)
    while job:
        job.delete()
        job = beanstalk.reserve(0)


#def semdmail(name, email):
#    print name, email

#semdmail_mqc = mq_client(semdmail)

#mq_server()
