#coding:utf-8

SHOW_LIMT = 3

def buzz_po_bind_user(i):
    new_reply_show = []
    for uid in user_id_list:
        if uid not in new_reply_show and user_id != uid:
            new_reply_show.append(uid)
            if len(new_reply_show) == SHOW_LIMT:
                break

    i.new_reply_show = [(z.id, z.name) for z in Zsite.mc_get_list(new_reply_show)]
    i.new_reply_count = max((len(set(user_id_list)) - SHOW_LIMT, 0))


