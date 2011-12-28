#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import cursor_by_table, McModel, McLimitA, McCache, McCacheA, Model, McNum
from txt2htm import RE_AT
from txt import txt_bind, txt_get, txt_new
from kv import Kv
from zsite_url import id_by_url


#from mq import mq_client
def mq_client(f):
    return f



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

def buzz_at_by_user_id_for_show(user_id):
    if mc_buzz_at_by_user_id_for_show.get(user_id) == 0:
        return 0
    begin_id = buzz_at_pos.get(user_id)
    result = tuple(reversed(BuzzAt.where(to_id=user_id, state=BUZZ_AT_SHOW).where('id>%s', begin_id).order_by('id').col_list(5, 0, BUZZ_AT_COL)))
    if result:
        buzz_at_pos.set(user_id, result[0][0])
        return result
    else:
        mc_buzz_at_by_user_id_for_show.set(user_id, 0)
        return 0

buzz_at_count = McNum(lambda user_id: BuzzAt.where(to_id=user_id, state=BUZZ_AT_SHOW).count() , 'BuzzAtCount:%s')

def mc_flush(user_id):
    buzz_at_count.delete(user_id)

def _buzz_at_list(user_id, limit, offset):
    return BuzzAt.where(to_id=user_id, state=BUZZ_AT_SHOW).order_by('id desc').col_list(limit, offset, BUZZ_AT_COL)



if __name__ == '__main__':
    pass

    print buzz_at_by_user_id_for_show(10001299)


