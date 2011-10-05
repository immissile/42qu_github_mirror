#coding:utf-8
import sys
from algorithm.merge import imerge
MAXINT = sys.maxint

def merge_iter(
    itemiter, id_list,  limit=MAXINT, begin_id=MAXINT
):
    count = 0
    for i in imerge(
        *[
            itemiter(i, begin_id)
            for i in
            id_list
        ]
    ):
        yield i
        count += 1
        if count >= limit:
            break
