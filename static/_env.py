
from os.path import abspath, dirname, normpath
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

PREFIX = normpath(dirname(dirname(abspath(__file__))))
if PREFIX not in sys.path:
    sys.path = [PREFIX] + sys.path
