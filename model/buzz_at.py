
from txt2htm import RE_AT


def at_id_list_by_txt(txt):

def buzz_at_new(user_id, po_id, txt ):
    ated = set(filter(bool, [id_by_url(i[2]) for i in RE_AT.findall(txt)]))
    for to_id in ated:
        buzz_new(user_id, to_id, CID_BUZZ_WORD_AT, po_id)

mq_buzz_at_new = mq_client(buzz_at_new)
