#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from index import index
from zsite_iter import zsite_keyword_iter

@single_process
def main():
    #rmtree(PATH)
    #makedirs(PATH)
    index(zsite_keyword_iter)


if __name__ == '__main__':
    main()
