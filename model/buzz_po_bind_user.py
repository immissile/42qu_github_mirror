#coding:utf-8
from zsite import Zsite
from itertools import chain

SHOW_LIMT = 3

def buzz_po_bind_user(po_list ,po_user_id_list, user_id=0):
    from model.po_pos import po_pos_get_last_reply_id
    user_dict = Zsite.mc_get_dict(chain(*po_user_id_list))
    result = []
    for i, user_id_list in zip(po_list, po_user_id_list):
        id = i.id
        new_reply_show = []

        for uid in user_id_list:
            if uid not in new_reply_show and user_id != uid:
                new_reply_show.append(uid)
                if len(new_reply_show) == SHOW_LIMT:
                    break

        new_reply_show = [
            (z.id, z.name) 
            for z in map(user_dict.get, new_reply_show)
        ]
        new_reply_count = max(
            (len(set(user_id_list)) - SHOW_LIMT, 0)
        )


        t = (
            id, 
            i.name, 
            new_reply_count, 
            new_reply_show, 
            po_pos_get_last_reply_id(user_id,id)
        )
        result.append(t)

    return result

