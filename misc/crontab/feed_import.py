#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model.feed_import import FeedImport, FEED_IMPORT_STATE_WITHOUT_TAG, FEED_IMPORT_STATE_INIT, FEED_IMPORT_STATE_POED, FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC, FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR, FEED_IMPORT_STATE_REVIEWED_SYNC, PoMetaUser, PoMeta
from config import ZSITE_DOUBAN_ID, ZSITE_UCD_CHINA_ID
from model.duplicate import Duplicator
from zkit.txt import format_txt
from config import DUMPLICATE_DB_PREFIX
from zkit.htm2txt import htm2txt
from zkit.single_process import single_process
from model.txt_img_fetch import txt_img_fetch
from model.url_short import url_short_id
from model.douban import DoubanUser, douban_feed_to_review_iter, douban_user_by_feed_id , title_normal
from model.site_sync import site_sync_new
from model.po_tag import po_tag_id_list_new
from model.po import po_note_new
from zkit.htm2txt import htm2txt, unescape
from time import sleep
from zkit.fanjian import utf8_ftoj
from model.feed_import_user import feed_import_user_new, feed_import_user_rm

import_feed_duplicator = Duplicator(DUMPLICATE_DB_PREFIX%'import_feed')

def feed_import_by_douban_feed():
    from model.douban import douban_feed_to_review_iter, DoubanUser
    for i in douban_feed_to_review_iter():
        #print i.id
        txt = i.htm.replace(
            '豆友', '网友'
        ).replace('豆油', '私信').replace('豆邮', '私信')
        #print i.id, i.title
        txt = htm2txt(txt)
        feed_import_new(
           ZSITE_DOUBAN_ID, i.id, i.title, txt, i.link,  i.like+i.rec
        )

def feed_import_new(zsite_id, rid, title, txt, url,  rank):
    title = utf8_ftoj(unescape(title))
    txt = utf8_ftoj(format_txt(txt))

    if import_feed_duplicator.txt_is_duplicate(txt):
        return
    #print zsite_id, rid, title
    #sleep(0.1)

    feed_user = user_by_feed_id_zsite_id(zsite_id, rid)
    if feed_user:
        po_meta_user_id = feed_user.id
    else:
        po_meta_user_id = 0

    new_feed = FeedImport(
        title=title,
        txt=txt,
        zsite_id=zsite_id,
        rid=rid,
        url=url,
        tag_id_list='',
        state=FEED_IMPORT_STATE_WITHOUT_TAG,
        rank=rank,
        po_meta_user_id=po_meta_user_id    
    )

    new_feed.save()
    id = new_feed.id
    import_feed_duplicator.set_record(txt, id)

    if feed_user:
        user_id = feed_user.user_id
        if user_id:
            feed_import_user_new(user_id, id)
    
    return new_feed


def feed2po_new():
    from zweb.orm import ormiter
    for feed in ormiter(
            FeedImport,
            'state>%s and state<%s'%(
                FEED_IMPORT_STATE_INIT,
                FEED_IMPORT_STATE_POED
            )
        ):
        feed_new(feed)

def user_by_feed_id_zsite_id(zsite_id, rid):
    feed_user = None
    if zsite_id == ZSITE_DOUBAN_ID:
        user = douban_user_by_feed_id(rid)
        if user:
            feed_user = PoMetaUser.get_or_create(name=user.name, cid=zsite_id)
            feed_user.url = feed_user.id
            feed_user.save()
    elif zsite_id == ZSITE_UCD_CHINA_ID:
        feed_user = PoMetaUser.get(rid) 
    return feed_user 

def feed_new(feed):
    txt = txt_img_fetch(feed.txt)
    zsite_id = feed.zsite_id
    feed_user = user_by_feed_id_zsite_id(zsite_id, feed.rid)
    if feed_user:
        user_id = feed_user.user_id
    else:
        user_id = 0
    id = feed.id

    if user_id:
        feed_import_user_rm(user_id, id)

    zsite_id = feed.zsite_id

    is_without_author = (
        (feed.state == FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC)
        or
        (feed.state == FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR)
    )

    if is_without_author:
        user_id = 0
        zsite_id = 0

    title = title_normal(feed.title)
    po = po_note_new(user_id, title, txt, zsite_id=zsite_id)

    if po:
        if not feed_user:
            feed_user_id = 0
        else:
            feed_user_id = feed_user.id

        record = PoMeta.get_or_create(id=po.id)
        record.user_id = feed_user_id
        record.url_id = url_short_id(feed.url)

        record.save()

        if not is_without_author:
            po.rid = record.id
            po.save()

        if feed.state >= FEED_IMPORT_STATE_REVIEWED_SYNC:
            site_sync_new(po.id)

        feed.state = FEED_IMPORT_STATE_POED
        feed.save()

        cid = feed.cid

        po_tag_id_list_new(po, feed.tag_id_list.split(' '), cid)
        #print po.link

@single_process
def main():
    feed2po_new()
    feed_import_by_douban_feed()


if __name__ == '__main__':
    main()

    #from zweb.orm import ormiter
    #for i in ormiter(FeedImport):
    #    zsite_id = i.zsite_id
    #    rid = i.rid
    #    user = user_by_feed_id_zsite_id(zsite_id, rid)
    #    if user:
    #        print zsite_id, rid
    #        i.po_meta_user_id = user.id
    #        i.save()

    #from zweb.orm import ormiter
    #for i in ormiter(FeedImport):
    #    i.title = unescape(i.title)
    #    print i.id
    #    i.save()
    # tag_admin_new(po_id, tag_id_list, rank)
