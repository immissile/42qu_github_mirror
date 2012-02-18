#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from name2id import NAME2ID
from model.po_by_tag import tag_alias_new
from model.autocomplete  import autocomplete_tag

def main():
    for k, v in NAME2ID.iteritems():
        alias, id = k, v
#        autocomplete_tag.append(alias, id)
        tag_alias_new(alias=alias, id=id)

if __name__ == '__main__':
    main()
