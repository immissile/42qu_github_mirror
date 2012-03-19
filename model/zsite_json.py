#coding:utf-8
from ico import ico_url_bind
from career import career_bind
from follow import follow_get_list
from motto import motto
from zkit.txt import cnenlen , cnenoverflow
from cid import CID_USER

def zsite_json(zsite_id, zsite_list):
    ico_url_bind(zsite_list)
    zsite_id_list = tuple(i.id for i in zsite_list)

    user_list = []
    for i in zsite_list:
        if i.cid == CID_USER:
            user_list.append(i)
    career_bind(user_list)

    motto_dict = motto.get_dict(zsite_id_list)

    result = []

    for i, is_follow in zip(
        zsite_list,
        follow_get_list(zsite_id, zsite_id_list)
    ):
        career = (' , '.join(filter(bool, i.career)) if i.cid==CID_USER else 0) or 0
        _motto = motto_dict.get(i.id) or 0
        if _motto:
            length = 14
            if not career:
                length += length
            _motto = cnenoverflow(_motto, length)[0]

        if is_follow and is_follow is not True:
            is_follow = 1
        result.append((
            i.id, #0 
            i.link, #1
            i.name, #2
            i.ico, #3
            career, #4
            i.cid , #5
            _motto , #6
            is_follow , #7
        ))

    return result

if __name__ == "__main__":
    pass



