#coding:utf-8

from autocomplete import autocomplete_tag
from autocomplete_user import autocomplete_user
from cid import CID_USER, CID_TAG
from itertools import izip_longest
from collections import defaultdict
from zkit.zitertools import roundrobin

def autocomplete(word):

    total = 10
    r1 = autocomplete_tag.id_rank_name_list_by_str(word, total)
    r2 = autocomplete_user.id_rank_name_list_by_str(word, total)

    result = defaultdict(list)
    for pos, (cid, i) in enumerate(roundrobin(
        ((CID_USER , i) for i in r2),
        ((CID_TAG  , i) for i in r1),

    )):
        if pos >= total:
            break
        result[cid].append(i)

    r = []
    for i in (CID_TAG, CID_USER, ):
        r.append((i, result[i]))

    return r


if __name__ == '__main__':
    from json import dumps
    print dumps(id_rank_name_list_by_autocomplete('z'))
    
