#coding:utf-8
import _env
from config import ZDATA_PATH
from ptag import PTAG
def train(filename, parser):
    for tag_id_list, txt in parser(filename):
        tag_id_set = set(tag_id_list)
        for tid in tuple(tag_id_set):
            tag_id_set.add(PTAG.get(tid,()))
        print tag_id_set

        #print filename, exist_id_list, txt

#    path = join(ZDATA_PATH_TRAIN_IDF, filename)
#
#    tofile = "%s.idf"%path
#    if exists(tofile):
#        #cmd = 'scp %s work@stdyun.com:%s'%(tofile, tofile)
#        #print cmd
#        #r = envoy.run(cmd)
#        #print r.std_out
#        return
#
#    if not exists(path):
#        return
#
#    df = Df()
#    count = 0
#    with open(path) as f:
#        for txt in parser(f):
#            df.append(txt)
#            if count%1000 == 1:
#                print filename, count
#            count += 1
#
#    df.tofile(tofile)
