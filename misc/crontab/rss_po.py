#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from htm2po.htm2po import htm2po_by_po
from model.rss import RssPo, RSS_PRE_PO, RSS_POED, RSS_RT_PO, RSS_SYNC
from zkit.single_process import single_process
from model.feed import feed_rt

def rss_po():
    for pre in RssPo.where(state=RSS_PRE_PO):
        htm2po_by_po(pre)
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
