#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.rss import unread_update, rss_subscribe
from zkit.single_process import single_process
from zkit.google.greader import Reader
from config import GREADER_USERNAME, GREADER_PASSWORD

@single_process
def main():
    greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
    rss_subscribe(greader)
    unread_update(greader)


if __name__ == '__main__':
    main()
