#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from htm2po.htm2po import htm2po_by_po
from model.rss import PrePo, RSS_PRE_PO,RSS_POED

def rss_po():
    for pre in PrePo.get(state = RSS_PRE_PO)
        htm2po_by_po(pre)
        pre.state = RSS_POED
        pre.save()


if __name__ == "__main__":
    rss_po()
