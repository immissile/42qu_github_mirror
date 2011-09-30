#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model

class SearchZsite(Model):
    pass

def search_new(id):
    SearchZsite.raw_sql("insert delayed into search_zsite (id) values (%s) on duplicate key update id=id", id)

if __name__ == "__main__":
    print search_new(10002411)


