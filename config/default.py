#coding:utf-8
import init_env
from hmako.lookup import TemplateLookup
import sys
from os.path import join

def prepare(o):
    o.SITE_DOMAIN = '42qu.test'
    o.PORT = 6666
    o.MYSQL_MAIN = 'zpage'
    o.PIC_URL = 'http://p.%s'%o.SITE_DOMAIN
    o.FS_URL = 'http://s.%s'%o.SITE_DOMAIN
    o.DEBUG = False
    return o

def debug(o):
    o.DEBUG = True

def finish(o):

    o.GOD_PORT = o.PORT + 11

    o.SITE_DOMAIN_SUFFIX = '.%s' % o.SITE_DOMAIN

    o.SITE_URL = '//%s' % o.SITE_DOMAIN
    o.SITE_HTTP = 'http://%s' % o.SITE_DOMAIN

    o.SENDER_NAME = o.SITE_DOMAIN

    HTM_PATH = join(init_env.PREFIX, 'htm')
    MAKOLOOKUP = TemplateLookup(
        directories=HTM_PATH,
        module_directory='/tmp/%s'%HTM_PATH.strip('/').replace('/', '.'),
        disable_unicode=True,
        encoding_errors='ignore',
        default_filters=['str', 'h'],
        filesystem_checks=o.DEBUG,
        input_encoding='utf-8',
        output_encoding=''
    )


    def render(htm, **kwds):
        mytemplate = MAKOLOOKUP.get_template(htm)
        return mytemplate.render(**kwds)
    o.render = render

    DB_HOST_MAIN = '%s:%s:%s:%s:%s' % (
        o.MYSQL_HOST, o.MYSQL_PORT, o.MYSQL_MAIN, o.MYSQL_USER, o.MYSQL_PASSWD
    )

    o.DB_CONFIG = {
        'main': {
            'master': o.DB_HOST_MAIN,
            'tables': (
                '*'
            )
        }
    }
    return o
