#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from config import SEARCH_DB_PATH
from mmseg.search import seg_txt_search, seg_title_search, seg_txt_2_dict
from os import makedirs
from os.path import join, exists
import xapian
from collections import defaultdict

PATH = join(SEARCH_DB_PATH, 'zsite')
if not exists(PATH):
    makedirs(PATH)

SEARCH_DB = xapian.WritableDatabase(PATH, xapian.DB_CREATE_OR_OPEN)

#print PATH

def flush_db():
    SEARCH_DB.flush()


@single_process
def index():
    from zsite_iter import zsite_keyword_iter
    for id, cid, rank, kw in zsite_keyword_iter():

        doc = xapian.Document()
        doc.add_value(0, id)
        doc.add_value(1, xapian.sortable_serialise(rank))
        doc.add_value(2, cid)

        for word, value in kw:
            if word:
                if not word.startswith('>'):
                    if len(word) < 254:
                        doc.add_term(word, value)

        key = '>%s' % id
        doc.add_term(key)
        SEARCH_DB.replace_document(key, doc)

    flush_db()


if __name__ == '__main__':
    index()
