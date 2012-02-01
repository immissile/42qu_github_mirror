#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import McModel
from zkit.txt_cleanup import feature_md5
from kyotocabinet import DB
from array import array

class DB_Kyoto(object):
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
    def __init__(self,db_path):
        self.db = DB_Kyoto(db_path)

    def set_record(self,txt,id):
        return self.db.set(txt, id)

    def find_duplicate(self,feature_list):
        result = set()
        count = 0
        for i in feature_list:
            db_get = self.db.get(i)
            if db_get:
                count+=1
                for j in db_get:
                    result.add(j)
        return [i for i in result], count

    def txt_is_duplicate(self,txt):
        feature_list = feature_md5(txt)
        found, count = self.find_duplicate(feature_list)
        if count>len(feature_list)*0.618:
            return True
        return False

#dup_db = DB_Kyoto(DUMPLICATE_DB)

#dub = Duplicator(DUMPLICATE_DB)
#
#set_record = dub.set_record
#find_duplicate = dub.find_duplicate
#txt_is_duplicate = dub.txt_is_duplicate


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
    #dup_db.set(a,3)
    #print find_duplicate(a)

    #from po import Po
    #for po in Po.where(cid = CID_NOTE,state=STATE_ACTIVE):
    #    Duplicate.insert(po.txt,po.id)
