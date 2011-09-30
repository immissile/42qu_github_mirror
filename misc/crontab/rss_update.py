#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.rss import unread_update
from zkit.single_process import single_process

@single_process
def main():
    unread_update()


if __name__ == '__main__':
    main()
