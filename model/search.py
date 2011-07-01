#!/usr/bin/env python
# -*- coding: utf-8 -*-
import init_db
from myconf.config import PREFIX, SEARCH_DB_PATH
from mmseg.search import seg_txt_search, seg_title_search, seg_txt_2_dict
from os.path import join
import xapian
from collections import defaultdict
import time
from mysite.util.pager import Pager, page_offset_limit
from mysite.model.man import Man
from mysite.model.about_me_htm import about_me_txt

def retry(func):
    def _(*args, **kwargs):
        tries = 2
        while tries:
            try:
                return func(*args, **kwargs)
            except :
                time.sleep(0.1)
                tries -= 1
                reload_db()
        return func(*args, **kwargs)
    return _

DATEBASE = None
ENQUIRE = None
def reload_db():
    global DATEBASE, ENQUIRE
    if DATEBASE:
        DATEBASE.reopen()
    else:
        DATEBASE = xapian.Database(join(SEARCH_DB_PATH, "man"))
        ENQUIRE = xapian.Enquire(DATEBASE)
        ENQUIRE.set_sort_by_value_then_relevance(1)

reload_db()




def make_query(keywords):
    if type(keywords) is unicode:
        keywords = keywords.encode("utf-8","ignore")

    and_query_list = []
    keywords = keywords.split(" ")

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

def _search_(enquire, keywords, offset=0, limit=50):
    if type(keywords) is xapian.Query:
        query = keywords
    else:
        query = make_query(keywords)
    enquire.set_query(query)
    matches = enquire.get_mset(offset, limit, None)
    return matches, matches.get_matches_estimated()


def _search(enquire, keywords, offset=0, limit=50):
    try:
        return _search_(enquire, keywords, offset, limit)
    except:
        reload_db()
    return _search_(enquire, keywords, offset, limit)


@retry
def search(keywords, offset, limit):
    e = ENQUIRE
    keywords = make_query(keywords)

    match, count = _search(e, keywords, offset, limit)
    r = []
    for m in match:
        doc = m.document
        rss_id = doc.get_value(0)
        r.append(rss_id)

    return Man.mc_get_list(r), count
