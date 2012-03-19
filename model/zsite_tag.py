#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCacheA, McCache, McCacheM, McLimitA, McNum
from tag import Tag, tag_new
from model.cid import CID_PO
from zweb.orm import ormiter
from po import Po, po_id_list


#CREATE TABLE  `zpage`.`zpage_tag` (
#  `id` int(10) unsigned NOT NULL auto_increment,
#  `zsite_id` int(10) unsigned NOT NULL,
#  `tag_id` int(10) unsigned NOT NULL,
#  PRIMARY KEY  (`id`),
#  KEY `tag_id` USING BTREE (`tag_id`),
#  KEY `zsite_id` (`zsite_id`,`tag_id`)
#) ENGINE=MyISAM DEFAULT CHARSET=binary;
#
#CREATE TABLE `zpage`.`zsite_tag_po` (
#  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
#  `zsite_tag_id` INTEGER UNSIGNED NOT NULL DEFAULT 0,
#  `po_id` INTEGER UNSIGNED NOT NULL,
#  `zsite_id` INTEGER UNSIGNED NOT NULL,
#  PRIMARY KEY (`id`),
#  INDEX `zsite_tag_id`(`zsite_tag_id`, `po_id`),
#  INDEX `po_id` ( `po_id`,`zsite_id`)
#)ENGINE = MyISAM;

ZSITE_TAG = (
    1, # 随笔杂记
    2, # 愿景计划
    3, # 职业感悟
    4, # 知识整理
    5, # 指点江山
    6, # 转载收藏
)

mc_zsite_tag_id_list_by_zsite_id = McCacheA('ZsiteTagIdListByZsiteId.%s')
mc_tag_id_list_by_zsite_id = McCacheA('TagIdListByZsiteId:%s')
mc_tag_by_po_id = McCacheM('TagIdByPoId:%s')
mc_po_id_list_by_zsite_tag_id = McLimitA('PoIdListByZsiteTagId:%s', 128)
zsite_tag_count = McNum(lambda id: ZsiteTagPo.where(zsite_tag_id=id).count(), 'ZsiteTagCount:%s')
zsite_tag_cid_count = McNum(lambda id, cid: ZsiteTagPo.where(zsite_tag_id=id, cid=cid).count(), 'ZsiteTagCount:%s')
mc_po_id_list_by_zsite_tag_id_cid = McLimitA('PoIdListByTagIdCid:%s', 128)
mc_zsite_tag_list_by_zsite_id_if_len = McCache('ZsiteTagListByZsiteIdIfLen*%s')

class ZsiteTag(McModel):
    pass

class ZsiteTagPo(McModel):
    pass

@mc_tag_id_list_by_zsite_id('{zsite_id}')
def tag_id_list_by_zsite_id(zsite_id):
    return ZsiteTag.where(zsite_id=zsite_id).order_by('id desc').col_list(col='tag_id')

@mc_zsite_tag_list_by_zsite_id_if_len('{zsite_id}')
def zsite_tag_list_by_zsite_id_if_len(zsite_id):
    tag_id_list = tag_id_list_by_zsite_id(zsite_id)
    tid = zsite_tag_id_list_by_zsite_id(zsite_id)
    r = []
    tid_list = []
    for i, count, t in zip(tag_id_list, zsite_tag_count.get_list(tid), tid):
        if count:
            r.append(i)
            tid_list.append(t)
    return tuple(zip(tid_list, Tag.value_by_id_list(r).itervalues()))


@mc_zsite_tag_id_list_by_zsite_id('{zsite_id}')
def zsite_tag_id_list_by_zsite_id(zsite_id):
    return ZsiteTag.where(zsite_id=zsite_id).order_by('id desc').col_list(col='id')

def link_by_zsite_id_tag_id(zsite_id, tag_id):
    t = ZsiteTag.get(zsite_id=zsite_id, tag_id=tag_id)
    if t:
        link = '/tag/%s'%t.id
    else:
        link = '/'
    return link

def zsite_tag_list_by_zsite_id(zsite_id):
    tag_id_list = tag_id_list_by_zsite_id(zsite_id)
    return Tag.value_by_id_list(tag_id_list)



def zsite_tag_new_by_zsite_id_tag_id(zsite_id, tag_id):
    zsite_tag = ZsiteTag.get_or_create(zsite_id=zsite_id, tag_id=tag_id)
    if not zsite_tag.id:
        zsite_tag.save()
        mc_flush_zsite_id(zsite_id)
    return zsite_tag.id

def zsite_tag_id_list_with_init(zsite_id):
    tag_id_list = tag_id_list_by_zsite_id(zsite_id)
    if not tag_id_list:
        for tag_id in ZSITE_TAG:
            zsite_tag_new_by_zsite_id_tag_id(zsite_id, tag_id)
        tag_id_list = list(reversed(ZSITE_TAG))
    return tag_id_list

def zsite_tag_list_by_zsite_id_with_init(zsite_id):
    tag_id_list = zsite_tag_id_list_with_init(zsite_id)
    return Tag.value_by_id_list(tag_id_list)



def zsite_tag_new_by_tag_id(po, tag_id=1):
    if not Tag.get(tag_id):
        tag_id = 1
    zsite_id = po.user_id
    po_id = po.id
    po_cid = po.cid

    if tag_id == 1: #初始化
        zsite_tag_id_list_with_init(zsite_id)

    id = zsite_tag_new_by_zsite_id_tag_id(zsite_id, tag_id)
    tag_po = ZsiteTagPo.get_or_create(
        po_id=po_id,
        zsite_id=zsite_id,
        cid=po_cid
    )

    pre_tag_id = tag_po.zsite_tag_id
    tag_po.zsite_tag_id = id
    tag_po.save()

    mc_tag_by_po_id.delete('%s_%s'%(zsite_id, po_id))

    from model.po_prev_next import mc_flush
    tag_po_id = tag_po.id

    if pre_tag_id:
        mc_po_id_list_by_zsite_tag_id.delete(pre_tag_id)
        zsite_tag_cid_count.delete(pre_tag_id, po_cid)
        mc_po_id_list_by_zsite_tag_id_cid.delete('%s_%s'%(pre_tag_id, po_cid))
        mc_flush(po, zsite_id, pre_tag_id)

    mc_po_id_list_by_zsite_tag_id.delete(id)
    mc_po_id_list_by_zsite_tag_id_cid.delete('%s_%s'%(id, po_cid))
    zsite_tag_cid_count.delete(id, po_cid)
    mc_flush(po, zsite_id, id)



def zsite_tag_new_by_tag_name(po, name):
    tag_id = tag_new(name)
    return zsite_tag_new_by_tag_id(po, tag_id)

def zsite_tag_id_mv(zsite_id, from_tag_id, to_tag_id=1):
    tag = ZsiteTag.get(zsite_id=zsite_id, tag_id=from_tag_id)

    for i in ormiter(ZsiteTagPo, 'zsite_tag_id=%s'%tag.id):
        i.zsite_tag_id = to_tag_id
        i.save()
        po_id = i.po_id
        mc_tag_by_po_id.delete('%s_%s'%(zsite_id, po_id))
    #print "delete zsite", zsite_id, from_tag_id
    ZsiteTag.where(zsite_id=zsite_id, tag_id=from_tag_id).delete()

    mc_flush_zsite_id(zsite_id)
    mc_flush_zsite_tag_id(from_tag_id)
    mc_flush_zsite_tag_id(to_tag_id)


def zsite_tag_rm_by_tag_id(zsite_id, tag_id):
    tag_id = int(tag_id)
    if tag_id == 1 or tag_id not in tag_id_list_by_zsite_id(zsite_id):
        return
    zsite_tag_id_mv(zsite_id, tag_id, 1)


def zsite_tag_rename(zsite_id, tag_id, tag_name):
    tag_id = int(tag_id)
    tag_name = tag_name.strip()
    if not tag_name:
        return
    tag = ZsiteTag.get(zsite_id=zsite_id, tag_id=tag_id)
    if not tag:
        return
    tag_id_new = tag_new(tag_name)
    ztn = ZsiteTag.get(zsite_id=zsite_id, tag_id=tag_id_new)
    if ztn:
        if ztn.tag_id != tag_id:
            zsite_tag_id_mv(zsite_id, tag_id, tag_id_new)
    else:
        tag.tag_id = tag_id_new
        tag.save()
        mc_flush_zsite_tag_id(zsite_id)


def mc_flush_zsite_id(id):
    mc_tag_id_list_by_zsite_id.delete(id)
    mc_zsite_tag_id_list_by_zsite_id.delete(id)
    mc_zsite_tag_list_by_zsite_id_if_len.delete(id)

def mc_flush_zsite_tag_id(id):
    zsite_tag_count.delete(id)
    mc_po_id_list_by_zsite_tag_id.delete(id)
    for cid in CID_PO:
        zsite_tag_cid_count.delete(id, cid)
        mc_po_id_list_by_zsite_tag_id_cid.delete('%s_%s'%(id, cid))

def zsite_tag_rm_by_po(po):
    id = po.id
    cid = po.cid
    for i in ZsiteTagPo.where(po_id=id):
        mc_flush_zsite_tag_id(i.zsite_tag_id)
        i.delete()
        from model.po_prev_next import mc_flush
        mc_flush(po, i.zsite_id, i.zsite_tag_id)
    mc_tag_by_po_id.delete('%s_%s' % (po.user_id, id))


@mc_tag_by_po_id('{zsite_id}_{po_id}')
def tag_by_po_id(zsite_id, po_id):
    c = ZsiteTagPo.raw_sql(
        'select zsite_tag_id from zsite_tag_po where zsite_id=%s and po_id=%s',
        zsite_id, po_id
    )
    r = c.fetchone()
    if r:
        zsite_tag_id = r[0]
        tag = ZsiteTag.mc_get(zsite_tag_id)
        tag_id = tag.tag_id
    else:
        return 0, 0, None
    return tag_id, zsite_tag_id, Tag.get(tag_id)

def zsite_tag_id_tag_name_by_po_id(zsite_id, po_id):
    return tag_by_po_id(zsite_id, po_id)[1:]

def tag_id_by_po_id(zsite_id, po_id):
    return tag_by_po_id(zsite_id, po_id)[0]


def tag_id_by_user_id_cid(zsite_id, cid):
    id_list = po_id_list(zsite_id, cid, True, 1, 1)
    if id_list:
        id = id_list[0]
        return tag_id_by_po_id(zsite_id, id)
    return 1


@mc_po_id_list_by_zsite_tag_id('{zsite_tag_id}')
def po_id_list_by_zsite_tag_id(zsite_tag_id, limit=None, offset=0):
    id_list = ZsiteTagPo.where(zsite_tag_id=zsite_tag_id).order_by('id desc').col_list(limit, offset, 'po_id')
    return id_list

@mc_po_id_list_by_zsite_tag_id_cid('{zsite_tag_id}_{cid}')
def po_id_list_by_zsite_tag_id_cid(zsite_tag_id, cid, limit=None, offset=0):
    return ZsiteTagPo.where(zsite_tag_id=zsite_tag_id, cid=cid).order_by('-po_id').col_list(limit, offset, 'po_id')

#def tag_po_classify(zsite_tag_id, cid, n=6):
#    pass

def count_po_list_by_zsite_tag_id_cid(zsite_tag_id, cid, limit=6):
    return (
        zsite_tag_cid_count(zsite_tag_id, cid),
        Po.mc_get_list(po_id_list_by_zsite_tag_id_cid(zsite_tag_id, cid, limit))
    )


#def zsite_tag_rm_by_user_id(user_id):
#    tag_list = zsite_tag_id_list_with_init(user_id)
#    for id in tag_list:
#        zsite_tag_rm_by_tag_id(user_id,id)


if __name__ == '__main__':
    from model.cid import CID_NOTE
    #print tag_id_by_user_id_cid(10000212, CID_AUDIO)
    #print zsite_tag_list_by_zsite_id_if_len(10000000)
    pass
    #print zsite_tag_cid_count(1, CID_NOTE)
    
