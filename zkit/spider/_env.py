import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from os.path import dirname, abspath, join
PWD = dirname(dirname(abspath(__file__)))
sys.path.append(dirname(PWD))
