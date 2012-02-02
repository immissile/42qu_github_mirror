#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model.import_feed import feed2po_new, zsite_id_by_douban_user_id,ImportFeed, IMPORT_FEED_STATE_INIT, DOUBAN_ZSITE_ID, IMPORT_FEED_CID_DICT
from model.duplicate import Duplicator
from zkit.txt import format_txt
from config import DUMPLICATE_DB_PREFIX
from zkit.htm2txt import htm2txt
from model.douban import douban_feed_to_review_iter, DoubanUser 

douban_duplicator = Duplicator(DUMPLICATE_DB_PREFIX%'douban')

def import_feed_by_douban_feed():
    for i in douban_feed_to_review_iter():
        import_feed_new(
            i.title, i.htm,  i.link, i.id, DOUBAN_ZSITE_ID
        )

def import_feed_new(title, txt, url, src_id, zsite_id, state=IMPORT_FEED_STATE_INIT):
    txt = format_txt(htm2txt(txt)).replace("豆友","网友").replace("豆油","私信").replace("豆邮","私信")
    if not douban_duplicator.txt_is_duplicate(txt):

       # douban_user = DoubanUser.get(author_id)
       # user_id = zsite_id_by_douban_user_id(douban_user)

        #cid = IMPORT_FEED_CID_DICT[zsite_id]

        new_feed = ImportFeed(
                title=title,
                txt=txt,
                zsite_id=zsite_id,
                state=state,
                rid=src_id,
                url=url,
                )

        new_feed.save()
        douban_duplicator.set_record(txt, new_feed.id)

        return new_feed


if __name__ == '__main__':
    feed2po_new()
    import_feed_by_douban_feed()
