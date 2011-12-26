#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache, McLimitM, McNum
from mq import mq_client
from buzz_at import buzz_at_new
from txt import txt_get

##CREATE TABLE `zpage`.`buzz_reply` (
##  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
##  `po_id` INTEGER UNSIGNED NOT NULL,
##  `user_id` INTEGER UNSIGNED NOT NULL,
##  `state` TINYINT UNSIGNED NOT NULL,
##  `update_time` INTEGER UNSIGNED NOT NULL,
##  PRIMARY KEY (`id`),
##  INDEX `Index_2`(`user_id`, `state`, `update_time`)
##)
##ENGINE = MyISAM;

BUZZ_STATE_SHOW = 30
BUZZ_STATE_HIDE = 20
BUZZ_STATE_RM   = 10

class BuzzReply(McModel):
    pass



def buzz_po_reply_new(from_id, reply_id, po_id, po_user_id):
    from po_pos import user_id_list_by_po_pos_buzz
    buzz_to = user_id_list_by_po_pos_buzz(po_id) 
    txt = txt_get(reply_id)
    excepted = buzz_at_new(from_id, po_id,txt)
    excepted.add(from_id)


    if from_id != po_user_id:
        buzz_to.add(po_user_id)

    buzz_to = buzz_to - excepted

    now = int(time())
    for user_id in :
        buzz_reply = BuzzReply.get_or_create(po_id=po_id, user_id=user_id)
        buzz_reply.update_time = now
        buzz_reply.state = BUZZ_STATE_SHOW
        buzz_reply.save()


mq_buzz_po_reply_new = mq_client(buzz_po_reply_new)

def buzz_po_reply_rm(reply_id):
    for i in ormiter(Buzz, 'cid=%s and rid=%s' % (CID_BUZZ_PO_REPLY, reply_id)):
        to_id = i.to_id
        i.delete()
        mc_flush(to_id)
        buzz_unread_update(to_id)

mq_buzz_po_reply_rm = mq_client(buzz_po_reply_rm)


def buzz_po_rm(po_id):
    to_id_list = set()
    po = Po.mc_get(po_id)
    to_id_list = set()
    for reply_id in po.reply_id_list():
        for i in ormiter(Buzz, 'cid=%s and rid=%s' % (CID_BUZZ_PO_REPLY, reply_id)):
            to_id_list.add(i.to_id)
            i.delete()
    for to_id in to_id_list:
        mc_flush(to_id)
        buzz_unread_update(to_id)

mq_buzz_po_rm = mq_client(buzz_po_rm)

if __name__ == "__main__":
    pass
