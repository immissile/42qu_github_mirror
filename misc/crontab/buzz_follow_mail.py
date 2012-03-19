#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from time import time
from collections import defaultdict
from model.buzz import Buzz, buzz_pos
from model.cid import CID_BUZZ_FOLLOW
from model.kv_misc import kv_int, KV_BUZZ_FOLLOW_POS
from model.mail import rendermail
from model.mail_notice import mail_notice_state
from model.user_mail import mail_by_user_id
from model.zsite import Zsite, ZSITE_STATE_VERIFY
from zkit.ordereddict import OrderedDict
from zkit.orderedset import OrderedSet
from zkit.single_process import single_process
from model.days import ONE_DAY

@single_process
def buzz_follow_mail():
    prev_pos = kv_int.get(KV_BUZZ_FOLLOW_POS)
    c = Buzz.raw_sql(
        'select max(id) from buzz where create_time<%s', int(time()) - ONE_DAY
    )
    pos = c.fetchone()[0]
    if pos > prev_pos:
        d = defaultdict(OrderedDict)

        for i in Buzz.where(cid=CID_BUZZ_FOLLOW).where('to_id=rid').where(
            'id>%s and id<=%s', prev_pos, pos
        ):
            id = i.id
            d[i.to_id][i.from_id] = i.id

        dd = defaultdict(OrderedSet)
        for to_id, _d in d.iteritems():
            if mail_notice_state(to_id, CID_BUZZ_FOLLOW):
                min_id = buzz_pos.get(to_id)
                for from_id, id in _d.iteritems():
                    if id > min_id:
                        dd[to_id].add(from_id)


        for to_id, li in dd.iteritems():

            mail = mail_by_user_id(to_id)
            name = Zsite.mc_get(to_id).name

            for from_id in li:

                from_user = Zsite.mc_get(from_id)
                career = from_user.career
                if from_user.state >= ZSITE_STATE_VERIFY and any(career):
                    rendermail(
                        '/mail/buzz/follow_new.htm', mail, name,
                        from_user=from_user,
                        format='html',
                        subject='%s ( %s ) 关注 你' % (
                            from_user.name,
                            ' , '.join(career),
                        )
                    )
                    #sleep(0.1)

        kv_int.set(KV_BUZZ_FOLLOW_POS, pos)


if __name__ == '__main__':
    buzz_follow_mail()
