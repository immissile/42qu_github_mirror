#coding:utf-8
import _env
from config import SITE_DOMAIN

def init_tag():
    from model.tag import tag_new, Tag
    from model.kv import mc
    print "#model/zsite_tag.py"
    print 'ZSITE_TAG = ('
    for tag in (
        '随笔杂记',
        '愿景计划',
        '职业感悟',
        '知识整理',
        '指点江山',
        '转载收藏',
    ):
        id = tag_new(tag)
        mc_key = Tag.__mc_id__%id
        mc.delete(mc_key)
        id = tag_new(tag)
        print '    %s, # %s'%(id, tag)
    print ')'

def init_buzz_sys():
    from model.buzz_sys import buzz_sys_htm
    BUZZ_SYS_INIT = (
        '不要恐慌 , 欢迎漫游42区 ... ...',
        '江山如画 , 一时多少豪杰 , <a href="http://hero.%s">点此浏览</a>' % SITE_DOMAIN,
        '欢迎讲述自己的人生故事 , <a href="/po/note">点此动笔</a>',
    )
    for seq, htm in enumerate(BUZZ_SYS_INIT, 1):
        buzz_sys_htm(htm, seq)

def init_db():
    init_tag()
    init_buzz_sys()

if __name__ == '__main__':
    init_db()
