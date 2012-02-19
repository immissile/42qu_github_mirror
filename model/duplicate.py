#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.txt_cleanup import feature_md5
from kyotocabinet import DB
from array import array
from collections import defaultdict
import sys

class DbKyoto(object):
    def __init__(self, db_file):
        self.db = DB()
        self.db_file = db_file
        if not self.db.open(db_file, DB.OWRITER | DB.OCREATE):
            print >> sys.stderr, 'open error: ' + str(self.db.error())

    def set(self, txt, po_id):
        feature_list = feature_md5(txt)
        for feature in feature_list:
            key = feature
            entry = self.get(key)
            if not entry:
                val = array('L', [po_id])
                if not self.db.set(key, val.tostring()):
                    print >> sys.stderr, 'open error: ' + str(self.db.error())
            else:
                val = array('L')
                val.fromstring(entry)
                if po_id not in val:
                    val.append(po_id)
                    self.db.set(key, val.tostring())
                return val

    def get(self, key):
        po_id = self.db.get(key)
        result = array('L')
        if po_id:
            result.fromstring(po_id)
        return result


class Duplicator(object):
    def __init__(self, db_path):
        self.db = DbKyoto(db_path)

    def set_record(self, txt, id):
        return self.db.set(txt, id)

    def __find_duplicate__(self, feature_list):
        result = defaultdict(int)
        for i in feature_list:
            for j in self.db.get(i):
                result[j] += 1
        return result

    def txt_is_duplicate(self, txt):
        feature_list = feature_md5(txt)

        if not feature_list:
            return []

        #print feature_list
        feature_list_len = float(len(feature_list))
        min_same_count = int(feature_list_len*0.618)+1

        result = []
        for id, same_count in self.__find_duplicate__(feature_list).iteritems():
            #print same_count
            if same_count > min_same_count:
                result.append((id, same_count/feature_list_len))

        return result


if __name__ == '__main__':
    a = '''
dsfdf 3
sdfdf 3啊的所发送的发送地方阿苏的发
sdfsdf
dfdf
d顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶
d
速度发送的发送的发送地方撒速度发送的发送的发送地方撒:w 速度发送的发送的发送地方撒:w 速度发送的发送的发送地方撒:w f
df
d
f
d
'''
    from config import DUMPLICATE_DB_PREFIX

    dup_db = Duplicator(DUMPLICATE_DB_PREFIX%'test2')
    dup_db.set_record(a, 3)
    print dup_db.txt_is_duplicate(a)

    #from po import Po
    #for po in Po.where(cid = CID_NOTE,state=STATE_ACTIVE):
    #    Duplicate.insert(po.txt,po.id)
