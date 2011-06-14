#coding:utf-8
import init_env

def init_tag():
    from model.tag import tag_new, Tag
    from model.kv import mc
    print 'TAG = ('
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

def init_db():
    init_tag()

if __name__ == '__main__':
    init_db()
