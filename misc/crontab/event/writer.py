#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zkit.lock_file import LockFile
import os.path as path

CURRNET_PATH = path.dirname(path.abspath(__file__))

class Writer(object):
    instance = None
    WRITTER_DICT = {}
    def __init__(self):
        pass

    def choose_writer(self,name):
        if name not in Writer.WRITTER_DICT:
            Writer.WRITTER_DICT[name]=LockFile(path.join(CURRNET_PATH, name),'wa')
        return Writer.WRITTER_DICT[name]

    @staticmethod
    def get_instance():
        if not Writer.instance:
            Writer.instance = Writer()
        return Writer.instance
        
