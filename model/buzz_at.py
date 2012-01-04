#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import cursor_by_table, McModel, McLimitA, McCache, McCacheA, Model, McNum, McCacheM
from txt2htm import RE_AT
from txt import txt_bind, txt_get, txt_new
from kv import Kv
from zsite_url import id_by_url
from zkit.algorithm.unique import unique

from mq import mq_client
#def mq_client(f):
#    return f



# buzz_at
# id
# from_id
# to_id
# po_id
# reply_id
# state

#CREATE TABLE `zpage`.`buzz_at` (
#  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
#  `from_id` INTEGER UNSIGNED NOT NULL,
#  `to_id` INTEGER UNSIGNED NOT NULL,
#  `reply_id` INTEGER UNSIGNED NOT NULL,
#  `state` TINYINT UNSIGNED NOT NULL DEFAULT 30,
#  `po_id` INTEGER UNSIGNED NOT NULL,
#  PRIMARY KEY (`id`),
#  INDEX `Index_2`(`to_id`, `state`, `id`),
#  INDEX `Index_3`(`po_id`)
#)
#ENGINE = MyISAM;

# buzz_at_pos
# id
# value

BUZZ_AT_SHOW = 30
BUZZ_AT_HIDE = 20
BUZZ_AT_RMED = 0

buzz_at_pos = Kv('buzz_at_pos', int)

class BuzzAt(Model):
    pass

def at_id_set_by_txt(txt):
    return set(filter(bool, [id_by_url(i[2]) for i in RE_AT.findall(txt)]))

def buzz_at_pos_set(id,pos):
    buzz_at_pos.set(id,pos)
    mc_buzz_at_by_user_id_for_show.set(id,0)
    buzz_at_user_count.set(id, 0)

def buzz_at_pos_set_max(id):
    reply_list = buzz_at_list(id,1,0)
    if reply_list:
        max_id = reply_list[0][0]
        buzz_at_pos_set(id,max_id)

def buzz_at_new(from_id, txt, po_id, reply_id=0):
    at_id_set = at_id_set_by_txt(txt)
    for to_id in at_id_set:
        buzz_at = BuzzAt(from_id=from_id, to_id=to_id, reply_id=reply_id, po_id=po_id, state=BUZZ_AT_SHOW)
        buzz_at.save()
        mc_flush(to_id)
        mc_buzz_at_by_user_id_for_show.delete(to_id)

    return at_id_set

mq_buzz_at_new = mq_client(buzz_at_new)


def buzz_at_reply_rm(reply_id):
    from model.reply import Reply
    txt = txt_get(reply_id)
    if not txt:
        return
    at_id_set = at_id_set_by_txt(txt)
    for to_id in at_id_set:
        BuzzAt.where(to_id=to_id, reply_id=reply_id).update(state=BUZZ_AT_RMED)
        mc_flush(to_id)

BUZZ_AT_COL = 'id,from_id,po_id,reply_id'

mc_buzz_at_by_user_id_for_show = McCache('BuzzAtByUserIdForShow:%s')

def buzz_at_dump_for_show(li):
    po_id_list = []
    reply_id_list = []
    for id, from_id, po_id, reply_id in li:
        po_id_list.append(po_id)
        if reply_id:
            reply_id_list.append(po_id)

    from model.reply import Reply
    from model.po import Po
    po_mc_get_dict = Po.mc_get_dict(po_id_list)
    result = []
    return result

mc_buzz_at_by_user_id_for_show = McCacheM('BuzzAtByUserIdForShow+%s')

@mc_buzz_at_by_user_id_for_show('{user_id}')
def buzz_at_by_user_id_for_show(user_id):
    from model.zsite import Zsite

    if mc_buzz_at_by_user_id_for_show.get(user_id) == 0:
        return ()

    begin_id = buzz_at_pos.get(user_id)
    #begin_id = 0
    result = tuple(reversed( BuzzAt.where(to_id=user_id, state=BUZZ_AT_SHOW).where('id>%s', begin_id).order_by('id').col_list(10, 0, 'id, from_id')))
    count = buzz_at_user_count(user_id)
    if result:
        result = unique(tuple(i[1] for i in result))[:3]
        count = buzz_at_user_count(user_id) - len(result)
        from model.zsite import Zsite
        result = Zsite.mc_get_list(result)
        return max(count, 0), tuple(i.name for i in result)
    return 0

buzz_at_user_count = McNum(
    lambda user_id: BuzzAt.raw_sql(
        'select count(DISTINCT from_id) from buzz_at where to_id=%s and state=%s and id>%s', user_id, BUZZ_AT_SHOW, buzz_at_pos.get(user_id)
    ).fetchone()[0] ,
    'BuzzAtUserCount+%s'
)

buzz_at_count = McNum(lambda user_id: BuzzAt.where(to_id=user_id, state=BUZZ_AT_SHOW).count(), 'BuzzAtCount+%s')

def mc_flush(user_id):
    buzz_at_user_count.delete(user_id)
    buzz_at_count.delete(user_id)
    mc_buzz_at_by_user_id_for_show.delete(user_id)

def buzz_at_col_list(user_id, limit, offset):
    return BuzzAt.where(to_id=user_id, state=BUZZ_AT_SHOW).order_by('id desc').col_list(limit, offset, BUZZ_AT_COL)

def buzz_at_list(user_id, limit, offset):
    po_id_list = []
    reply_id_list = []
    user_id_list = []
    id_list = []
    for id,from_id,po_id,reply_id in buzz_at_col_list(user_id, limit, offset):
        id_list.append(id)
        po_id_list.append(po_id)
        reply_id_list.append(reply_id) 
        user_id_list.append(from_id)
   
    from model.zsite import Zsite
    from model.po import Po
    from model.reply import Reply
    return tuple(zip(        
        id_list, 
        Zsite.mc_get_list(user_id_list),
        Po.mc_get_list(po_id_list),
        Reply.mc_get_list(reply_id_list),
    ))


        

if __name__ == '__main__':
    pass
    #print buzz_at_list(     10031395, 10, 0)
    print buzz_at_user_count(10000000)
    print buzz_at_by_user_id_for_show(10000000)
    mc_buzz_at_by_user_id_for_show.delete(10000000)
