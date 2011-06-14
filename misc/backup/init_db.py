#coding:utf-8
import init_env

def init_tag():
    from model.tag import Tag
    for tag in (
        '随笔杂记',
        '愿景计划',
        '职业感悟',
        '知识整理',
        '指点江山',
        '思绪飘零',
        '转载收藏',
    ):
        print Tag.get_or_create_id_by_value(tag)

def init_db():
    init_tag()

if __name__ == '__main__':
    init_db()
