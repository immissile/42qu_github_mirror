#!/usr/bin/env python
# -*- coding:utf-8 -*-
import _env
from model.zsite import Zsite
from model.tag import Tag

TAG = (
    (1, '随笔杂记'),
    (2, '愿景计划'),
    (3, '职业感悟'),
    (4, '知识整理'),
    (5, '指点江山'),
    (6, '转载收藏'),
)

def init_tag():
    for id, name in TAG:
        Tag.set(id, name)


CHANNEL = (
    (10036807, '产品'),
    (10036808, '公司'),
    (10036809, '招聘'),
    (10036810, '思考'),
    (10036811, '随笔'),
    (10036812, '传奇'),
    (10036813, '技术'),
    (10036814, '创业'),
)

def init_channel():
    for id, name in CHANNEL:
        Zsite(id=id, name=name).save()


if __name__ == '__main__':
    init_tag()
    init_channel()
