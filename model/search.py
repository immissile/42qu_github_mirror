#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _db
from collections import defaultdict
from config import SEARCH_DB_PATH
from mmseg.search import seg_txt_search, seg_title_search, seg_txt_2_dict
from model.zsite import Zsite
from model.txt import txt_get
from model.motto import motto_get
from os.path import join
from time import sleep
import xapian
from model.cid import CID_USER, CID_SITE

DATEBASE = None
ENQUIRE = None

def reload_db():
    global DATEBASE, ENQUIRE
    if DATEBASE:
        DATEBASE.reopen()
    else:
        DATEBASE = xapian.Database(join(SEARCH_DB_PATH, 'zsite'))
        ENQUIRE = xapian.Enquire(DATEBASE)
        ENQUIRE.set_sort_by_value_then_relevance(1, False)

reload_db()


def retry(func):
    def _(*args, **kwargs):
        n = 2
        while n:
            try:
                return func(*args, **kwargs)
            except :
                sleep(0.1)
                n -= 1
                reload_db()
        return func(*args, **kwargs)
    return _


def make_query(keywords):
    if type(keywords) is unicode:
        keywords = keywords.encode('utf-8', 'ignore')

    and_query_list = []
    keywords = keywords.split(' ')

    for keyword in keywords:
        if len(keyword) > 2 and keyword.startswith('"') and keyword.endswith('"'):
            and_query_list.append(
                xapian.Query(
                    keyword[1:-1],
                    1
                )
            )
        else:
            t = []
            word2dict = seg_txt_2_dict(keyword)
            for word, value in word2dict.iteritems():
                if word != keyword:
                    t.append(
                        xapian.Query(
                            word,
                            1
                        )
                    )
            kt = xapian.Query(keyword, 1)
            if t:
                if len(t) > 1:
                    query = xapian.Query(xapian.Query.OP_AND, t)
                    query = xapian.Query(xapian.Query.OP_OR, [kt, query])
                else:
                    query = xapian.Query(xapian.Query.OP_OR, [kt, t[0]])
            else:
                query = kt
            and_query_list.append(query)
    #for i in and_query_list:
    #print "!!!",i
    if len(and_query_list) > 1:
        query = xapian.Query(xapian.Query.OP_AND, and_query_list)
    else:
        query = and_query_list[0]

    return query


@retry
def _search(enquire, keywords, cid=None, offset=0, limit=50):
    if type(keywords) is xapian.Query:
        query = keywords
    else:
        query = make_query(keywords)
    enquire.set_query(query)

    if cid is None:
        matches = enquire.get_mset(offset, limit, None)
    else:
        match = xapian.ValueSetMatchDecider(2, True)
        match.add_value(str(cid)) 
        matches = enquire.get_mset(offset, limit, None, match)
    return matches, matches.get_matches_estimated()


def search_user(keywords, offset, limit):
    return search(keywords, CID_USER,  offset, limit)


def search_site(keywords, offset, limit):
    return search(keywords, CID_SITE,  offset, limit)




@retry
def search(keywords, cid, offset, limit):
    e = ENQUIRE
    keywords = make_query(keywords)

    match, count = _search(e, keywords, cid, offset, limit)
    r = []
    for m in match:
        doc = m.document
        rss_id = doc.get_value(0)
        r.append(rss_id)

    return Zsite.mc_get_list(r), count

if __name__ == '__main__':
    print search_user('awerewar', 0, 111)
    print search_site('awerewar', 0, 111)

    cid = CID_USER



