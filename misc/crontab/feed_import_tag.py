#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from zkit.single_process import single_process
from model.feed_import import FeedImport, FEED_IMPORT_STATE_INIT, FEED_IMPORT_STATE_WITHOUT_TAG
from zweb.orm import ormiter
from model.tag_admin import tag_admin_new
from zdata.idf.tfidf import tag_id_rank_list_by_txt, ID2NAME
from operator import itemgetter

@single_process
def main():
    for i in ormiter(FeedImport, "state=%s"%FEED_IMPORT_STATE_WITHOUT_TAG):
        txt = "%s\n%s"%(
            i.title,
            i.txt
        )

        tag_id_rank_list = tag_id_rank_list_by_txt(txt)[:7]
        tag_id_list = map(itemgetter(0), tag_id_rank_list)

        i.tag_id_list = " ".join(map(str,tag_id_list))
        i.state = FEED_IMPORT_STATE_INIT
        i.save()

        tag_admin_new(i.id, tag_id_list, i.rank)

        print i.id, i.title, i.url
        for k, v in tag_id_rank_list:
            print k, v,
            for j in ID2NAME[k]:
                print j,
            print ""
        print ">>>"*7


if "__main__" == __name__:
    main()

