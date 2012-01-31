#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import McModel
from zkit.txt_cleanup import feature_md5


def find_duplicate(txt):
    feature_list = feature_md5(txt)
    count = 0
    for i in feature_list:
        if Duplicate.mc_get(i):
            count+=1
        if len(feature_list)*0.618<count:
            return True
            break
    return False

class Duplicate(McModel):
    @staticmethod
    def insert(txt,id):
        feature_list = feature_md5(txt)
        for feature in feature_list:
            dul = Duplicate.get_or_create(id=feature)
            if not dul.doc_id_list:
                dul.doc_id_list="%s"%id
            else:
                dul.doc_id_list+=" %s"%id
            dul.save()

if __name__ == '__main__':
    a = '''
Use this command to anonymously check out the latest project source code:
今dfdfdf年央视春晚请走不少老面孔，起dfasdf初是语言类节目的顶梁柱频频出局，没想到一贯稳定的主持人阵容上也同声共气，飞走了央视当家主持人周涛，迎来了85后小美女李思思。1986年出生的李思思2005年以大学生身份参加《挑战主持人》节目，连任8期擂主后，次年以全国选拔赛季军的身份进入央视。在央视她主持《舞蹈世界》，主持过两届央视舞蹈大赛，并不显山露水，这次登上春晚舞台前，她离春晚最近的一次是主持2011年春晚前的“倒计8小时”直播节目。前天，李思思在春晚彩排的一号演播大厅露面，外界想到了她将登上春晚舞台，却没想到她替下的竟是周涛。
adfdf
　　asdfas另外，记者昨天获悉，影视演员王珞丹(微博)将在开场歌舞中亮相。开场歌舞作为春晚第一炮，不仅要给观众最好的“第一眼”印象，同时也是过去一年里当红艺人的展示舞台。

　　对比近asdfasdf几年的春晚开场，虎年春晚以歌舞大联欢引导主持出场，兔年春晚则主打“山楂树组合”，到龙年春晚由王珞丹等“新鲜”面孔混搭朱军、李咏、老毕组成的“霸气男人帮”阵容，“鲜”字概念逐年突显。
'''
    print find_duplicate(a)
