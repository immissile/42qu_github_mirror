#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model

class SearchZsite(Model):
    pass

def search_new(id):
    if not SearchZsite.get(id):
        SearchZsite(id=id).save()
