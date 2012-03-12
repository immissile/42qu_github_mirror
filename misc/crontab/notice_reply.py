#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_REPLY_NUM
from model.reply import  Reply
from model.cid import CID_NOTE, CID_USER
from collections import defaultdict
from time import sleep
from model.po_pos import po_pos_get
from model.po import Po
from model.zsite import Zsite
from model.career import career_current
from model.user_mail import mail_by_user_id
from model.mail import rendermail

def reply_notice_mail(po_id, li):
    po = Po.mc_get(po_id)
    if not (po and po.zsite_id != po.user_id):
        return

    li = Zsite.mc_get_list(li)

    if not li:
        return

    pos, state = po_pos_get(po.user_id, po_id)
    #print pos
    if pos != -1:
        return

    zsite = Zsite.mc_get(po.user_id)

    if zsite and zsite.cid == CID_USER:

        mail = mail_by_user_id(po.user_id)

        if mail:

            li0 = li[0]

            name_list = [li0.name]
            name_list.extend(career_current(li0.id))
            name_title = ' , '.join(filter(bool, name_list))

            if len(li) > 1:
                subject = '%s人 回复 %s ( %s 等 )'%(
                    len(li) , po.name , name_title
                )
            else:
                subject = '%s 回复 %s'%(name_title, po.name)


            rendermail( '/mail/notice/notice_reply.htm', mail, zsite.name, format='html', subject=subject, reply_list=li, po=po, zsite=zsite)

            mail = 'zsp042@gmail.com'

            rendermail( '/mail/notice/notice_reply.htm', mail, zsite.name, format='html', subject=subject, reply_list=li, po=po, zsite=zsite)


@single_process
def notice_reply():
    pre_pos = kv_int.get(KV_REPLY_NUM)

    #print pre_pos; pre_pos = 0

    c = Reply.raw_sql( 'select max(id) from reply where cid = %s', CID_NOTE)

    pos = c.fetchone()[0]

    if pos > pre_pos:
        d = defaultdict(set)

        for i in Reply.where(cid=CID_NOTE).where( 'id>%s and id<=%s', pre_pos, pos):
            po_id = i.rid
            user_id = i.user_id
            d[po_id].add(user_id)

        for po_id, li in d.iteritems():
            reply_notice_mail(po_id, li)

        kv_int.set(KV_REPLY_NUM, pos)


if __name__ == '__main__':
    #print po_pos_get(10001135, 10102793)
    notice_reply()
    #print po_pos_get(10006891,10102798)
    pass
