#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model.feed_import import feed2po_new, zsite_id_by_douban_user_id, FeedImport, FEED_IMPORT_STATE_INIT, FEED_IMPORT_CID_DICT
from config import ZSITE_DOUBAN_ID
from model.duplicate import Duplicator
from model.zsite import Zsite
from zkit.txt import format_txt
from config import DUMPLICATE_DB_PREFIX
from zkit.htm2txt import htm2txt
from zkit.single_process import single_process

tag_getter = GetTag()

import_feed_duplicator = Duplicator(DUMPLICATE_DB_PREFIX%'import_feed')

def feed_import_by_douban_feed():
    from model.douban import douban_feed_to_review_iter, DoubanUser
    for i in douban_feed_to_review_iter():
        feed_import_new(
            i.title, i.htm, i.link, i.id, ZSITE_DOUBAN_ID
        )

def feed_import_new(title, txt, url, src_id, zsite_id, tag_id_list='', state=FEED_IMPORT_STATE_INIT):
    txt = format_txt(htm2txt(txt))

    if import_feed_duplicator.txt_is_duplicate(txt):
        return 
    
    if zsite_id == ZSITE_DOUBAN_ID:
        txt = txt.replace('豆友', '网友').replace('豆油', '私信').replace('豆邮', '私信')

    new_feed = FeedImport(
        title=title,
        txt=txt,
        zsite_id=zsite_id,
        state=state,
        rid=src_id,
        url=url,
        tag_id_list='',
        
    )

    #TODO
    if not tag_id_list:
        name_list = tag_getter.get_tag(txt)
        for tag_name in  name_list:
            zsite_list.append(Zsite.get(name=tag_name))

    new_feed = FeedImport(
        title=title,
        txt=txt,
        zsite_id=zsite_id,
        state=state,
        rid=src_id,
        url=url,
        tag_id_list=tag_id_list,
    )

    new_feed.save()
    import_feed_duplicator.set_record(txt, new_feed.id)

    return new_feed


@single_process
def main():
    #feed2po_new()
    feed_import_by_douban_feed()


if __name__ == '__main__':
    main()
