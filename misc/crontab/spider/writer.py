#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zkit.lock_file import LockFile
from model._db import Model
import os.path as path
from hashlib import md5
from yajl import dumps

CURRNET_PATH = path.dirname(path.abspath(__file__))



class Spider(Model):
    @staticmethod
    def insert(title, tags, content, author, rating, url, reply_list, pic_list):
        key = url_key_builder(url)
        entry = Spider.get_or_create(url_hash=key)
        entry.title = title
        entry.tags = dumps(tags)
        entry.content = content
        entry.author = author
        entry.rating = rating
        entry.url = url
        entry.url_hash = key
        entry.reply_list = dumps(reply_list)
        entry.pic_list = dumps(pic_list)
        entry.save()

def url_is_fetched(url):
    key = url_key_builder(url)
    url = Spider.where(url=key)
    return url

def url_key_builder(url):
    key = md5(url).hexdigest()
    return key

class Writer(object):
    instance = None
    WRITTER_DICT = {}
    def __init__(self):
        pass

    def choose_writer(self, name):
        if name not in Writer.WRITTER_DICT:
            Writer.WRITTER_DICT[name] = LockFile(path.join(CURRNET_PATH, name), 'a')
        return Writer.WRITTER_DICT[name]

    @staticmethod
    def get_instance():
        if not Writer.instance:
            Writer.instance = Writer()
        return Writer.instance

