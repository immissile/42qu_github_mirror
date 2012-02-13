#coding:utf-8
import _env
from misc.spider.zhihu_topic_url2id import ID2MY
from misc.spider.zhihu_topic_data_20120211 import ZHIHU_TOPIC
from model.zsite import Zsite
from model.cid import CID_TAG
from zkit.pprint import pprint


#S = """
#10228502 互联网
#10225318 手机应用
#10222498 Microsoft Word
#10229885 米饭网
#10232540 垃圾回收 / 计算机科学
#10224348 Windows Live Messenger
#""".strip().split("\n")
#id_list = [
#    i.split(" ")[0] for i in S
#]
#print id_list
#for i in Zsite.mc_get_list(id_list):
#    print i
#    i.delete()

#ID2MY = dict((k,v) for k,v in ID2MY.iteritems() if Zsite.mc_get(v))
#print """
#import _env
#ID2MY = 
#""",
#pprint(ID2MY)
#print """
#
#if __name__ == "__main__":
#    
#    url2id = {}
#    for i in ZHIHU_TOPIC:
#        url = i[2] or i[1]
#        id = i[0]
#        rank = i[-1]
#
#        if id in ID2MY:
#            url2id[ID2MY[id] ] = rank 
#
#
#    from zkit.pprint import pprint
#
#    pprint(url2id)
#"""
RESULT = {}
for tag in Zsite.where(cid=CID_TAG):
    name_list = map(str.strip, tag.name.split('/'))
    for name in name_list:
        RESULT[name.replace('·', '.').lower()] = tag.id

for i in ZHIHU_TOPIC:
    id = i[0]
    if id not in ID2MY:
        continue
    rename = i[-1]
    for name in rename:
        name = name.lower()
        if name in RESULT and RESULT[name] != ID2MY[id]:
            zsite = Zsite.mc_get(ID2MY[id])
            print zsite.id, zsite.name
            zsite = Zsite.mc_get(RESULT[name])
            print zsite.id, zsite.name
        else:
            continue


print """
#coding:utf-8
TAG2ID = 
""",
pprint(RESULT)


