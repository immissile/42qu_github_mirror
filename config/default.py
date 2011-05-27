#coding:utf-8
import init_env
from hmako.lookup import TemplateLookup
import sys
from os.path import join

def prepare(o):
    o.SITE_DOMAIN = '42qu.test'
    o.PORT = 6666
    o.MYSQL_MAIN = 'zpage'
    o.PIC_DOMAIN = "p.%s"%o.SITE_DOMAIN
    o.FS_DOMAIN = "s.%s"%o.SITE_DOMAIN
    o.DEBUG = False
    return o

def debug(o):
    o.DEBUG = True

def finish(o):

    o.PIC_PATH = "/mnt/zpage"
    o.GOD_PORT = o.PORT + 10
    o.PIC_URL = 'http://%s'%o.PIC_DOMAIN
    o.FS_URL = 'http://%s'%o.FS_DOMAIN

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

def load(self, *args):
    PREPARE = [
        prepare
    ]
    FINISH = [
        finish
    ]

    def load(name):
        try:
            mod = __import__(
                name,
                globals(),
                locals(),
                [],
                -1
            )
        except ImportError:
            print "NO CONFIG %s"%name
            return
        for i in name.split(".")[1:]:
            mod = getattr(mod,i)
        prepare = getattr(mod, "prepare", None)

        if prepare:
            PREPARE.append(prepare)

        finish = getattr(mod, "finish", None)
        if finish:
            FINISH.append(finish)
    for i in args:
        load(i)
    funclist = PREPARE+list(reversed(FINISH))
    for _ in funclist:
        _(self)
    return self

