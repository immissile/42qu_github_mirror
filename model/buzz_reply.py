#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache, McLimitM, McNum
from buzz_at import buzz_at_new
from txt import txt_get

#from mq import mq_client
def mq_client(f):
    return f

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

BUZZ_REPLY_STATE_SHOW = 30
BUZZ_REPLY_STATE_HIDE = 20
BUZZ_REPLY_STATE_RM   = 10
BUZZ_REPLY_STATE_PO_RMED   = 0

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
        buzz_reply.state = BUZZ_REPLY_STATE_SHOW
        buzz_reply.save()


mq_buzz_po_reply_new = mq_client(buzz_po_reply_new)

def buzz_po_reply_rm(po_id, reply_id):
    from po_pos import PoPos, STATE_BUZZ
    from model.po import Po
    po = Po.mc_get(po_id)
    if po and reply_id >= po.reply_id_last:
        for user_id in PoPos.where(po_id=po_id, state=STATE_BUZZ).where("po_pos>%s",reply_id).col_list(col="user_id"):
            BuzzReply.where(po_id=po_id, user_id=user_id, state=BUZZ_REPLY_STATE_SHOW).update(state=BUZZ_REPLY_STATE_HIDE)

mq_buzz_po_reply_rm = mq_client(buzz_po_reply_rm)


def buzz_po_rm(po_id):
    BuzzReply.where(po_id=po_id).update(state=BUZZ_REPLY_STATE_PO_RMED )

mq_buzz_po_rm = mq_client(buzz_po_rm)


def buzz_reply_show_list_by_user_id(user_id):
    pass

if __name__ == "__main__":
    pass
