#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from kyotocabinet import DB
from array import array
from zkit.zitertools import lineiter
from yajl import loads


def main():
    db = DB()
    if not db.open("bayes.kch", DB.OWRITER | DB.OCREATE):
        return

    with open("word_tf.txt") as word_tf:
        for line in word_tf:
            line = line.strip()
            word, bayes_list = loads(line)
            print word
            if bayes_list:
                ar = array('I')
                ar.fromlist(lineiter(bayes_list))
                db[word] = ar.tostring()

if "__main__" == __name__:
    main()

