#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.po_recommend import po_recommend_new
from model.vote import Vote

def main():
    votes=Vote.where()
    for vote in votes:
        new_rec = po_recommend_new(vote.po_id,vote.user_id,'')
if __name__ == '__main__':
    main()
