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

def reply_notice_mail(po_id, li):
    po = Po.mc_get(po_id)
    if not (po and po.zsite_id != po.user_id):
       return 

    li = Zsite.mc_get_list(li)

    if not li:
        return

    pos, state = po_pos_get(po.user_id, po_id)

    if pos != -1:
        return 

    zsite = Zsite.mc_get(po.user_id)

    if zsite and zsite.cid==CID_USER:

        mail = mail_by_user_id(po.user_id)

        if mail:

            if len(li) > 1:
                title = career_current(po.user_id)
                name_list = [li[0].name]
                name_list.extend(title)
                subject = "%s人 回复 %s ( %s 等 )"%(
                    len(li) , po.name , " , ".join(name_list)
                )
            else:
                subject = "%s 回复 %s"%(li[0], po.name)


            print mail
            subject = mail+" "+subject
            mail = "zsp007@gmail.com"

            rendermail(
                '/mail/notice/notice_reply.htm',
                mail,
                zsite.name,
                format='html',
                subject = subject,
                reply_list=li,
                po = po,
                zsite = zsite
            )


@single_process
def notice_reply():
    pre_pos = kv_int.get(KV_REPLY_NUM)
    print pre_pos
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
    notice_reply()
