#!/usr/bin/env python
#coding:utf-8
from os.path import abspath, dirname, join, normpath
from glob import glob

"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from os.path import abspath, dirname, join, normpath
import sys
from os.path import abspath, dirname, join, normpath
from hmako.lookup import TemplateLookup

#初始化python的查找路径
PREFIX = normpath(dirname(dirname(abspath(__file__))))
if PREFIX not in sys.path:
    sys.path = [PREFIX] + sys.path

%s

HTM_PATH = join(dirname(dirname(abspath(__file__))), 'htm')

MAKOLOOKUP = TemplateLookup(
    directories=HTM_PATH,
    module_directory='/tmp/%s'%HTM_PATH.strip('/').replace('/', '.'),
    disable_unicode=True,
    encoding_errors='ignore',
    default_filters=['str', 'h'],
    filesystem_checks=DEBUG,
    input_encoding='utf-8',
    output_encoding=''
)

def render(htm, **kwds):
    mytemplate = MAKOLOOKUP.get_template(htm)
    return mytemplate.render(**kwds)
"""
PREFIX = normpath(dirname(abspath(__file__)))

for filename in glob(join(PREFIX,"%s/template/*.py"%PREFIX)):
    print filename

#from mako.template import Template

#with open(join(PREFIX, "config/nginx/template.conf")) as template:
#    TEMPLATE = Template(template.read())

#def render_conf(templa):
#    txt = TEMPLATE.render(this=cls())
#    print cls.__name__, cls().host
#    with open(join(PREFIX, "config/"%cls.__name__.lower()), "w") as w:
#        w.write(txt)

#class ConfBase(object):
#    @property
#    def pic_host(self):
#        return self.config.PIC_URL[7:]
#
#    @property
#    def pic_path(self):
#        return self.config.PIC_PATH
#
#    @property
#    def fs_host(self):
#        return self.config.FS_URL[7:]
#
#
#    @property
#    def god_port(self):
#        return self.config.GOD_PORT
#
#    @property
#    def host(self):
#        config = self.config
#        host = {
#            config.SITE_DOMAIN: [config.PORT, ]
#        }
#        return host
#
#    @property
#    def fs_path(self):
#        return "/home/%s/zpage/static"%self.__class__.__name__.lower()
#
#    @property
#    def config(self):
#        if not hasattr(self, "_config"):
#            config = load(self.config_file)
#            self._config = config
#        return self._config
#
#def load(setting):
#    import conf
#    import config
#    setting = __import__(setting, globals(), locals(), [], -1)
#    for k in vars(setting):
#        if not k.startswith("__"):
#            setattr(conf, k, getattr(setting, k))
#    print conf.SITE_DOMAIN
#    reload(config)
#    return config
#
#@render_conf
#class Yup(ConfBase):
#    config_file = "conf_yup"
#
#@render_conf
#class Zjd(ConfBase):
#    config_file = "conf_zjd"
#
#@render_conf
#class Zuroc(ConfBase):
#    config_file = "conf_zuroc"
#

#@render_conf
#class Work(ConfBase):
#    config_file = "conf_work"
#    host = {
#        "42qu.me" : [
#            22000,
#            22001
#        ],
#    }
#    fs_path = "/home/work/zpage/web/static"
#
#@render_conf
#class WorkDev(ConfBase):
#    config_file = "host_dev_nuva"
#    fs_path = "/home/work/zpage/web/static"
#
