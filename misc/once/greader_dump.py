import _env
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from zkit.google.greader import Reader
reader = Reader('42qu.com', '')


for i in reader.feed('feed/http://feed.feedzshare.com'):
    print i
    sys.stdout.flush()



for i in reader.feed('feed/http://www.feedzshare.com/s/t/1/rss'):
    print i
    sys.stdout.flush()


for i in reader.feed('feed/http://www.feedzshare.com/s/t/3/rss'):
    print i
    sys.stdout.flush()
