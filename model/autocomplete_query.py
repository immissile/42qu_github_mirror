#coding:utf-8
from model.autocomplete import autocomplete_tag
from model.autocomplete_user import autocomplete_user
from model.cid import CID_USER, CID_TAG
from itertools import izip_longest
from collection import defaultdict
from zkit.zitertools import roundrobin

def id_rank_name_list_by_autocomplete(word):

    total = 10
    r1 = autocomplete_tag.id_rank_name_list_by_str(word, total)
    r2 = autocomplete_user.id_rank_name_list_by_str(word, total)

    result = defaultdict(list) 
    for cid, i in roundrobin(
        ((CID_TAG  , i) for i in r1),
        ((CID_USER , i) for i in r2),

    ):
        
        result[cid].appned(i)
    
    return result 
    


