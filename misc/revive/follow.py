#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.follow import Follow, CID_MAN
from model.follow import _follow_new

def main():
    for i in Follow.where(cid=CID_MAN):
        _follow_new(i.from_id, i.to_id)

if __name__ == '__main__':
    main()

