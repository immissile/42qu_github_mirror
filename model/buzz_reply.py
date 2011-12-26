#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache, McLimitM, McNum

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

class BuzzReply(McModel):
    pass



def buzz_po_reply_new(from_id, reply_id, po_id, po_user_id):
    from txt import txt_get
    from po_pos import po_pos_state, STATE_MUTE
    txt = txt_get(reply_id)
    ated = set(filter(bool, [id_by_url(i[2]) for i in RE_AT.findall(txt)]))

    followed = set([i.from_id for i in ormiter(Follow, 'to_id=%s' % from_id)])
    buzz_to = set([i.user_id for i in ormiter(PoPos, 'po_id=%s and state=%s' % (po_id, STATE_BUZZ))])
    excepted = set([from_id, po_user_id])

    if from_id != po_user_id:
        buzz_new(from_id, po_user_id, CID_BUZZ_PO_REPLY, reply_id)

    for user_id in ((ated | followed | buzz_to) - excepted):
        buzz_new(from_id, user_id, CID_BUZZ_PO_REPLY, reply_id)
        po_pos_state(user_id, po_id, STATE_MUTE)

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
