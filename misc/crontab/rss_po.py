#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from htm2po.htm2po import htm2po_by_po
from model.rss import RssPo, RSS_PRE_PO, RSS_POED, RSS_RT_PO, RSS_SYNC
from zkit.single_process import single_process
from model.feed import feed_rt

def rss_po():
    rss_feed_new = set()
    rss_feed = set()

    for pre in RssPo.where(state=RSS_PRE_PO):
        print pre.id, pre.title, pre.link
        po = htm2po_by_po(pre)
        if po:
            rss_id = pre.rss_id
            #print po.id
            if rss_id not in rss_feed:
                rss_feed.add(rss_id)
                if RssPo.where(state=RSS_POED, rss_id=rss_id).count():
                    rss_feed_new.add(rss_id)

            if rss_id in rss_feed_new:
                po.feed_new()


        pre.state = RSS_POED
        pre.save()

    for pre in RssPo.where(state=RSS_RT_PO):
        po = htm2po_by_po(pre)
        if po:
            feed_rt(0, po.id)
        pre.state = RSS_POED
        pre.save()

@single_process
def main():
    rss_po()

if __name__ == '__main__':
    main()

    #from model.po import Po,feed_rm
    #from model.rss import RssPoId
    ##feed_rm(10247794)
    ##feed_rm(10247793)
    #print RssPoId.get(po_id=10247794)
    #for i in RssPo.where(user_id=10000076):
    #    rss_po = RssPoId.get(rss_po_id=i.id)
    #    if rss_po:
    #        po = Po.mc_get( rss_po.po_id  )
    #        feed_rm(po.id)
    #        print po.id
