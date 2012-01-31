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
from model.po_by_tag import PoZsiteTag, zsite_tag_new_po, get_or_create_tag
from model.po import po_note_new, Po
from model.duplicate import find_duplicate

CURRNET_PATH = path.dirname(path.abspath(__file__))

def main():
    dic = fromfile(path.join(CURRNET_PATH, 'tag2id'))
    for k, v in dic.iteritems():
        site = get_or_create_tag(k)
        print site.name
        print site.id

def parse_data():
    with open(path.join(CURRNET_PATH, 'ucdchina.data')) as f:
        for line in f:
            data = loads(line)
            title = data[0]
            content, img_list = htm2txt(data[1])
            author = data[2]
            tag_list = data[3]
            print title, ','.join([i[0] for i in tag_list])
            po = po_note_new(64278, title, content, zsite_id=64278)
            for tag in tag_list:
                _tag = get_or_create_tag(tag[0])
                zsite_tag_new_po(po, float(tag[1]), _tag.id)

if __name__ == '__main__':
    parse_data()
