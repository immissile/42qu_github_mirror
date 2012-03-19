import sys
import time
#print dir(memlink)

from memlink.memlinkclient import MEMLINK_OK, MemLinkClient, MEMLINK_VALUE_VISIBLE
from struct import pack
from array import array

READ_PORT = 11001
WRITE_PORT = 11002

class MemLinkError(Exception):
    def __init__(self, code):
        super(MemLinkError, self).__init__()
        print code
        self.code = code


memlink = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)

class MemLinkIntList(object):
    def __init__(self, key_template):
        self.key_template = key_template

    def create_list(self, key):
        key = self.key_template%key
        ret = memlink.create_list(key, 32, '')
        if ret != MEMLINK_OK:
            raise MemLinkError(ret)

    def insert(self, key, value, pos=-1):
        key = self.key_template%key
        value = pack('I', value)
        print repr(value)
        ret = memlink.insert(key, value, pos, '')
        if ret != MEMLINK_OK:
            raise MemLinkError(ret)

    def range(self, key, limit, offset=0, kind=MEMLINK_VALUE_VISIBLE):
        key = self.key_template%key
        ret, result = memlink.range(key, kind, offset, limit, '')
        if ret != MEMLINK_OK:
            raise MemLinkError(ret)
        #print result.list()
        result_list = result.list()
        print repr(result_list[0][0])
        print result_list
        result = array('I').fromstring(''.join([i[0] for i in result_list]))
        return result

memlink_zsite_feed = MemLinkIntList('ZsiteFeed:%s')
key = 8
memlink_zsite_feed.create_list(key)
memlink_zsite_feed.insert(key, 321344)
for i in memlink_zsite_feed.range(key, 32):
    print i

raise
from memlink.memlinkclient import *
key = 'haha'

def insert(*args):
    try:
        start = int(args[0])
        num = int(args[1])
    except:
        start = 0
        num = 1000

    try:
        val = '%012d' % int(args[2])
    except:
        val = None

    print 'insert:', start, num, val

    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)

    ret = m.create_list(key, 12, '32:32:2')
    if ret != MEMLINK_OK:
        print 'create haha error!', ret
        #return

    for i in xrange(start, start + num):
        if not val:
            val2 = '%012d' % i
        else:
            val2 = val
        print 'insert:', val2
        mstr = '%d:%d:1' % (i, i)
        ret = m.insert(key, val2, mstr, i)
        if ret != MEMLINK_OK:
            print 'insert error:', ret, i
            return

    m.destroy()

def delete(*args):
    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)
    val = '%012d' % int(args[0])
    print 'delete:', val
    ret = m.delete(key, val)
    if ret != MEMLINK_OK:
        print 'delete error:', ret, val
        return

    m.destroy()

    return

    for i in xrange(1, 300):
        print 'del %012d' % (i*2)
        ret = m.delete(key, '%012d' % (i*2))
        if ret != MEMLINK_OK:
            print 'delete error:', ret, i*2
            return

    m.destroy()


def range(*args):
    try:
        kind = args[0]

        if kind.startswith('vis'):
            kind = MEMLINK_VALUE_VISIBLE
        elif kind.startswith('tag'):
            kind = MEMLINK_VALUE_ZSITE_TAGDEL
        elif kind.startswith('all'):
            kind = MEMLINK_VALUE_ALL
        else:
            print 'kind error! must visible/tagdel/all'
            return
    except:
        kind = MEMLINK_VALUE_VISIBLE

    try:
        frompos = int(args[1])
        slen = int(args[2])
    except:
        frompos = 0
        slen = 1000

    try:
        mask = args[3]
    except:
        mask = ''

    print 'ALL:%d, VISIBLE:%d, ZSITE_TAGDEL:%d' % (MEMLINK_VALUE_ALL, MEMLINK_VALUE_VISIBLE, MEMLINK_VALUE_ZSITE_TAGDEL)
    print 'range kind:%d, from:%d, len:%d, mask:%s' % (kind, frompos, slen, mask)

    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)

    ret, recs = m.range(key, kind, mask, frompos, slen)
    if ret != MEMLINK_OK:
        print 'range error:', ret
        return

    print recs.count
    items = recs.root
    while items:
        print items.value, repr(items.mask)
        items = items.next

    m.destroy()

def dump(*args):
    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)
    ret = m.dump()
    if ret != MEMLINK_OK:
        print 'dump error!', ret
    m.destroy()


def clean(*args):
    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)
    ret = m.clean(key)
    if ret != MEMLINK_OK:
        print 'clean error!', ret
    m.destroy()

def stat(*args):
    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)
    ret, stat = m.stat(key)
    if ret != MEMLINK_OK:
        print 'stat error!', ret
    print stat
    m.destroy()

def stat_sys(*args):
    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)
    ret, stat = m.stat_sys()
    if ret != MEMLINK_OK:
        print 'stat_sys error!', ret
    print stat
    m.destroy()


def ping(*args):
    try:
        count = int(args[1])
    except:
        count = 1000
    print 'ping count:', count
    start = time.time()
    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)
    for i in xrange(0, count):
        ret = m.ping()
        if ret != MEMLINK_OK:
            print 'ping error:', ret
            return
    m.destroy()
    end = time.time()

    print 'use time:', end - start, 'speed:', count / (end-start)

def lpush(*args):
    try:
        start = int(args[0])
        num = int(args[1])
    except:
        start = 0
        num = 1000

    try:
        val = '%012d' % int(args[2])
    except:
        val = None

    print 'lpush:', start, num, val

    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)

    ret = m.create_list(key, 12, '1')
    if ret != MEMLINK_OK:
        print 'create haha error!', ret
        #return

    for i in xrange(start, start + num):
        if not val:
            val2 = '%012d' % i
        else:
            val2 = val
        print 'lpush:', val2
        ret = m.lpush(key, val2, '1')
        if ret != MEMLINK_OK:
            print 'lpush error:', ret, i
            return

    m.destroy()

def rpush(*args):
    try:
        start = int(args[0])
        num = int(args[1])
    except:
        start = 0
        num = 1000

    try:
        val = '%012d' % int(args[2])
    except:
        val = None

    print 'lpush:', start, num, val

    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)

    ret = m.create_list(key, 12, '1')
    if ret != MEMLINK_OK:
        print 'create haha error!', ret
        #return

    for i in xrange(start, start + num):
        if not val:
            val2 = '%012d' % i
        else:
            val2 = val
        print 'rpush:', val2
        ret = m.rpush(key, val2, '1')
        if ret != MEMLINK_OK:
            print 'rpush error:', ret, i
            return

    m.destroy()

def lpop(*args):
    try:
        count = int(args[0])
    except:
        count = 1
    print 'lpop count:', count
    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)
    ret, result = m.lpop(key, count)
    if ret != MEMLINK_OK:
        print 'lpop error:', ret
        return
    print 'lpop result:', result.count
    item = result.root
    while item:
        print item.value, item.mask
        item = item.next

    m.destroy()

def rpop(*args):
    try:
        count = int(args[0])
    except:
        count = 1
    print 'rpop count:', count
    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)
    ret, result = m.rpop(key, count)
    if ret != MEMLINK_OK:
        print 'rpop error:', ret
        return
    print 'rpop result:', result.count
    item = result.root
    while item:
        print item.value, item.mask
        item = item.next

    m.destroy()

def sortlistinsert(*args):
    try:
        start = int(args[0])
        num = int(args[1])
    except:
        start = 0
        num = 1000

    try:
        val = '%012d' % int(args[2])
    except:
        val = None

    print 'insert:', start, num, val

    m = MemLinkClient('127.0.0.1', READ_PORT, WRITE_PORT, 10)

    ret = m.create_sortlist(key, 12, '1', MEMLINK_VALUE_STRING)
    if ret != MEMLINK_OK:
        print 'create haha error!', ret
        #return

    for i in xrange(start, start + num):
        if not val:
            val2 = '%012d' % i
        else:
            val2 = val
        print 'insert:', val2
        ret = m.sortlist_insert(key, val2, '1')
        if ret != MEMLINK_OK:
            print 'insert error:', ret, i
            return

    m.destroy()




if __name__ == '__main__':
    action = sys.argv[1]
    args = []
    if len(sys.argv) > 2:
        args.extend(sys.argv[2:])

    func = globals()[action]
    func(*args)



