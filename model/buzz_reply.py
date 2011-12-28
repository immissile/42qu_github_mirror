#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from buzz_at import buzz_at_new, buzz_at_reply_rm
from txt import txt_get

from mq import mq_client
#def mq_client(f):
#    return f

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
BUZZ_REPLY_STATE_RM = 10
BUZZ_REPLY_STATE_PO_RMED = 0

class BuzzReply(McModel):
    pass



def buzz_po_reply_new(from_id, reply_id, po_id, po_user_id):
    from po_pos import user_id_list_by_po_pos_buzz
    buzz_to = user_id_list_by_po_pos_buzz(po_id)
    txt = txt_get(reply_id)
    excepted = buzz_at_new(from_id, txt, po_id, reply_id)

    for user_id in excepted:
        buzz_reply_hide(user_id, po_id)

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
        for user_id in PoPos.where(po_id=po_id, state=STATE_BUZZ).where('po_pos>%s', reply_id).col_list(col='user_id'):
            BuzzReply.where(po_id=po_id, user_id=user_id, state=BUZZ_REPLY_STATE_SHOW).update(state=BUZZ_REPLY_STATE_HIDE)
            mc_flush(user_id)
    buzz_at_reply_rm(reply_id)

mq_buzz_po_reply_rm = mq_client(buzz_po_reply_rm)


def buzz_po_rm(po_id):
    for user_id in BuzzReply.where(po_id=po_id, state=BUZZ_REPLY_STATE_SHOW).col_list(col='user_id'):
        mc_flush(user_id)

    BuzzReply.where(po_id=po_id).update(state=BUZZ_REPLY_STATE_PO_RMED )


mq_buzz_po_rm = mq_client(buzz_po_rm)

mc_po_id_list_by_buzz_reply_user_id = McCacheA('PoIdListByBuzzReplyUserId:%s')

@mc_po_id_list_by_buzz_reply_user_id('{user_id}')
def po_id_list_by_buzz_reply_user_id(user_id):
    return BuzzReply.where(user_id=user_id, state=BUZZ_REPLY_STATE_SHOW).order_by('update_time desc').col_list(7, 0, 'po_id')


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

def buzz_reply_hide_or_rm_by_user_id(user_id):
    for i in po_id_list_by_buzz_reply_user_id(user_id):
        buzz_reply_hide_or_rm(i)
    mc_flush(user_id)

def mc_flush(user_id):
    mc_po_id_list_by_buzz_reply_user_id.delete(user_id)
    mc_po_list_by_buzz_reply_user_id.delete(user_id)

mc_po_list_by_buzz_reply_user_id = McCacheM('PoListByBuzzReplyUserId:%s')

@mc_po_list_by_buzz_reply_user_id('{user_id}')
def po_list_by_buzz_reply_user_id(user_id):
    from model.po import Po
    from model.po_pos import po_pos_get
    from model.reply import Reply
    from model.zsite import Zsite

    show_limt = 3
    id_list = po_id_list_by_buzz_reply_user_id(user_id)
    po_list = Po.mc_get_list(id_list)

    for i in po_list:
        pos = po_pos_get(user_id, i.id)[0]
        new_reply_id_list = []
        for reply_id in i.reply_id_list():
            if reply_id > pos:
                new_reply_id_list.append(reply_id)

        user_id_list = []
        for reply in Reply.mc_get_list(reversed(new_reply_id_list)):
            user_id_list.append(reply.user_id)

        new_reply_show = []
        for uid in user_id_list:
            if uid not in new_reply_show and user_id != uid:
                new_reply_show.append(uid)
                if len(new_reply_show) == show_limt:
                    break

        i.new_reply_show = [(z.id, z.name) for z in Zsite.mc_get_list(new_reply_show)]
        i.new_reply_count = max((len(set(user_id_list)) - show_limt, 0))

    result = []
    for po in po_list:
        t = (po.id, po.name, po.new_reply_count, po.new_reply_show)
        result.append(t)
    return result

if __name__ == '__main__':
    pass
    user_id = 10000000
    for i in po_list_by_buzz_reply_user_id(user_id):
        print i
