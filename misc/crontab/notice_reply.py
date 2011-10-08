#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_REPLY_NUM
from model.reply import reply_notice_mail

@single_process
def notice_reply():
    pre_pos = kv_int.get(KV_REPLY_NUM)
    c = Reply.raw_sql(
            'select max(id) from reply where cid = %s',CID_NOTE
            )
    pos = c.fetchone()[0]
    if pos > pre_pos:
        d = defaultdict(set)

        for i in Reply.where(cid = CID_NOTE).where(
                'id>%s and id <= %s',pre_pos, pos
                ):
            po_id = i.rid
            usr_id = i.user_id
            d[po_id].add(usr_id)

        for po_id, li in d.iteritems():
            reply_notice_mail(po_id,li)
            sleep(0.1)

        kv_int.set(KV_REPLY_NUM, pos)


if __name__ == "__main__":
    notice_reply()
