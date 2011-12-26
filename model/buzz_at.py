#!/usr/bin/env python
# -*- coding: utf-8 -*-
from txt2htm import RE_AT
from mq import mq_client



def buzz_at_new(user_id, po_id, txt ):
    at_id_set = set(filter(bool, [id_by_url(i[2]) for i in RE_AT.findall(txt)]))

    for to_id in at_id_set:
        #TODO
        #buzz_new(user_id, to_id, CID_BUZZ_WORD_AT, po_id)
        pass

    return at_id_set

mq_buzz_at_new = mq_client(buzz_at_new)
