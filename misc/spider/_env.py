import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from os.path import dirname, abspath
PWD = dirname(abspath(__file__))
sys.path.append(dirname(dirname(PWD)))


import zkit.spider 
import config
config.DISABLE_LOCAL_CACHED = True
