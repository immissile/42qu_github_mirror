#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA
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
    if buzz_to:
        now = int(time())
        for user_id in buzz_to:
            buzz_reply = BuzzReply.get_or_create(po_id=po_id, user_id=user_id)
            buzz_reply.update_time = now
            buzz_reply.state = BUZZ_REPLY_STATE_SHOW
            buzz_reply.save()
            mc_flush(user_id)


mq_buzz_po_reply_new = mq_client(buzz_po_reply_new)

def buzz_po_reply_rm(po_id, reply_id):
    from po_pos import PoPos, STATE_BUZZ
    from model.po import Po
    po = Po.mc_get(po_id)
    if po and reply_id >= po.reply_id_last:
        for user_id in PoPos.where(po_id=po_id, state=STATE_BUZZ).where("po_pos>%s",reply_id).col_list(col="user_id"):
            BuzzReply.where(po_id=po_id, user_id=user_id, state=BUZZ_REPLY_STATE_SHOW).update(state=BUZZ_REPLY_STATE_HIDE)
            mc_flush(user_id)

mq_buzz_po_reply_rm = mq_client(buzz_po_reply_rm)


def buzz_po_rm(po_id):
    for user_id in BuzzReply.where(po_id=po_id, state=BUZZ_REPLY_STATE_SHOW).col_list(col="user_id"):
        mc_flush(user_id)

    BuzzReply.where(po_id=po_id).update(state=BUZZ_REPLY_STATE_PO_RMED )


mq_buzz_po_rm = mq_client(buzz_po_rm)

mc_po_id_list_by_buzz_reply_user_id = McCacheA("PoIdListByBuzzReplyUserId:%s")

@mc_po_id_list_by_buzz_reply_user_id("{user_id}")
def po_id_list_by_buzz_reply_user_id(user_id):
    BuzzReply.where(user_id=user_id, state=BUZZ_REPLY_STATE_SHOW).order_by("update_time desc").col_list(0, 7, "po_id")


def buzz_reply_hide_or_rm(id):
    buzz = BuzzReply.get(id=id)
    if buzz:
        state = buzz.state
        if state == BUZZ_REPLY_STATE_SHOW :
            buzz.state = BUZZ_REPLY_STATE_RM
            buzz.save() 
            from model.po_pos import po_pos_state_mute
            po_pos_state_mute(buzz.user_id, buzz.po_id)
               
def buzz_reply_hide(user_id, po_id):
    buzz_reply = BuzzReply.get(
        user_id=user_id, po_id=po_id, state=BUZZ_REPLY_STATE_SHOW
    )
    if buzz_reply:
        buzz_reply.state = BUZZ_REPLY_STATE_HIDE
        buzz_reply.save() 
        if buzz_reply.id in po_id_list_by_buzz_reply_user_id(user_id):
            mc_flush(user_id)
 
def po_id_list_by_buzz_reply_user_id_rm(user_id):
    for i in po_id_list_by_buzz_reply_user_id(user_id):
        buzz_reply_hide_or_rm(i)
    mc_flush(user_id)

def mc_flush(user_id):
    mc_po_id_list_by_buzz_reply_user_id.delete(user_id)

if __name__ == "__main__":
    pass
