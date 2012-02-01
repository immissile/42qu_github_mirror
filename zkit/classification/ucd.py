#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import _env
from zkit.tofromfile import tofile, fromfile
from os import path
from model.zsite_site import zsite_new, ZSITE_STATE_SITE_PUBLIC
from model.cid import CID_TAG
from model.zsite import Zsite
from zkit.htm2txt import htm2txt
from yajl import loads
from model.po_by_tag import PoZsiteTag, zsite_tag_po_new, tag_by_name
from model.po import po_note_new, Po, po_rm
from model.duplicate import txt_is_duplicate, set_record
from model.txt_img_fetch import txt_img_fetch

CURRNET_PATH = path.dirname(path.abspath(__file__))

def main():
    dic = fromfile(path.join(CURRNET_PATH, 'tag2id'))
    for k, v in dic.iteritems():
        site = tag_by_name(k)
        print site.name
        print site.id

def parse_data():
    with open(path.join(CURRNET_PATH, 'ucdchina.data')) as f:
        for line in f:
            data = loads(line)
            title = data[0]
            content = htm2txt(data[1])
            content = txt_img_fetch(content)
            author = data[2]
            tag_list = data[3]
            print title, ','.join([i[0] for i in tag_list])
            po = po_note_new(64278, title, content, zsite_id=64278)

            if txt_is_duplicate(content):
                po_rm(64278, po.id)
            else:
                set_record(content, po.id)
                for tag in tag_list:
                    _tag = tag_by_name(tag[0])
                    zsite_tag_po_new(_tag.id, po, float(tag[1]))

if __name__ == '__main__':
    parse_data()
