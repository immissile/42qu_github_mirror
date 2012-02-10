#coding:utf-8

import _env
from collections import defaultdict
from mmseg import seg_txt
from yajl import loads
from zdata.tfidf.idf import idf_zhihu
from zdata.bayes.train import TAG2ID, WORD2ID 
from zdata.bayes.kyoto_db import DB_Kyoto
from zkit.sp_txt import sp_txt

import sys;
reload(sys); sys.setdefaultencoding('utf-8')

ID2TAG = TAG2ID.id2word()

class GetTag(object):
    def __init__(self ):
        self.idf = idf_zhihu()
        self.db = DB_Kyoto('bayes.kch')

    def get_tag(self, txt):
        topic_rank = defaultdict(float)
        tfidf_list = sorted(self.idf.tf_idf(txt), key=lambda x:x[1], reverse=True)
        average_tfidf = sum([i[1] for i in tfidf_list])/float(len(tfidf_list))
        tfidf_list = [ i for i in tfidf_list if i[1]>average_tfidf]


        for (word, word_tfidf), word_id in zip(
            tfidf_list,
            WORD2ID.id_list_by_word_list(i[0] for i in tfidf_list)
        ):
            topic_items_dict  = self.db.get(word_id)
            if topic_items_dict:
                for topic_id, bayes in topic_items_dict:
                    topic_rank[topic_id] += (word_tfidf*bayes)

        topic_rank = sorted(topic_rank.iteritems(), key=lambda x:x[1], reverse=True)
        txt = txt.lower()
        if topic_rank:
            rank_avg = float(sum(i[1] for i in topic_rank))/len(topic_rank)
            for topic_id, rank in topic_rank[:50]:
                '''
                推荐主题做二元分词, 如果文章中没有, 则去掉. 
                '''
                topic = ID2TAG[topic_id]
                rank_t = rank/rank_avg
                for seg in sp_txt(topic):
                    if seg in txt:
                        yield topic, rank_t
                        break

                if rank_t<6:
                    break


if __name__ == '__main__':
    txt = '''
Pinterest的一些思考
周末在家的时候，除了重构了部分代码以外，最多的时候想的就是Pinterest这件事情。最近太多关关于Pinterest的新闻出来了，包括花瓣拿到的4.5 M 美金的投资。包括估值巨高的Pinterest的各种事情。
其实回过来看Pinterest和最象它的豆瓣相册。附上我们对：豆瓣相册统计
Pinterest的模式更为松散，确切的说，Pinterest的模式的信息粒度是单张照片，一花一世界。Pinterest的松散的方式让逛变得没有目的。
豆瓣相册的模式信息粒度突出的其实是单个相册。相册和单个照片不一样，豆瓣热门的相册大部分都以：xxxx美食教学，xxxx的20种方法，最温馨的xxxx个瞬间这样的标题。我们是一个一个相册的获得信息，在看到单个照片前我们通常是带有一定的目的的。
另外一个很类似的东西是微博的图片分享，但是绝大多数微博的图片分享都局限于自己的美食经历，自己的穿衣打扮，和生活状态。
这是三个完全不同的目的导向的产品，虽然他们面向的人群和内容是有交集，有共性的，但是他们最终的走向的却是不同的内容和受众，看pinterest的人，看豆瓣相册的人，看微博相册的人，人都是不一样的，目的也都是不一样的。
在中国分享的人群更少，大家耗在微博和qq空间，甚至豆瓣的时间都很多。而且从一个宏观的大角度上来看，中国远远还不到饱暖思淫欲的时刻，中国人很多时候还是在想如何在淘宝赚钱，或者说更多人还停留在网址导航，停留在打开电脑只看qq的年代。
我一直坚信的是，facebook和twitter打通了一条信息的流动的通路，但是通往信息最终散落的地方的很多重要的，有价值的内容其实并没有 得到完全的承载。因此如果说前一阵（5年左右时间）的大事情是信息的传播，社会化的话，我相信在一段时间过去最大的价值是各种有价值的信息的承载和细分。
这些细分已经逐渐的显现出来了。包括，音乐类Spotify。问答类Quora。旅行类daodao等等。在一段时间内的细分市场会更加垂直和深入，以不同的方式展示和聚合最有价值的部分信息，真正为社会化的网络搭建的这条信息通道输送内容。
那下一个是Pinterest吗？它能不能在中国顺利的成长？我觉得借鉴一下delicious的经验就可以知道这是很难的一条路，yupoo也没有完全复制Flickr的成功。或许或许，在中国Pinterest的机会不在花瓣，而在于美丽说。    
'''
    cla = GetTag()
    for i in cla.get_tag(txt):
        print i

#ID2TAG = TAG2ID.id2word()
#
#if __name__ == '__main__':
#
#    txt = '''
#Pinterest的一些思考
#周末在家的时候，除了重构了部分代码以外，最多的时候想的就是Pinterest这件事情。最近太多关关于Pinterest的新闻出来了，包括花瓣拿到的4.5 M 美金的投资。包括估值巨高的Pinterest的各种事情。
#其实回过来看Pinterest和最象它的豆瓣相册。附上我们对：豆瓣相册统计
#Pinterest的模式更为松散，确切的说，Pinterest的模式的信息粒度是单张照片，一花一世界。Pinterest的松散的方式让逛变得没有目的。
#豆瓣相册的模式信息粒度突出的其实是单个相册。相册和单个照片不一样，豆瓣热门的相册大部分都以：xxxx美食教学，xxxx的20种方法，最温馨的xxxx个瞬间这样的标题。我们是一个一个相册的获得信息，在看到单个照片前我们通常是带有一定的目的的。
#另外一个很类似的东西是微博的图片分享，但是绝大多数微博的图片分享都局限于自己的美食经历，自己的穿衣打扮，和生活状态。
#这是三个完全不同的目的导向的产品，虽然他们面向的人群和内容是有交集，有共性的，但是他们最终的走向的却是不同的内容和受众，看pinterest的人，看豆瓣相册的人，看微博相册的人，人都是不一样的，目的也都是不一样的。
#在中国分享的人群更少，大家耗在微博和qq空间，甚至豆瓣的时间都很多。而且从一个宏观的大角度上来看，中国远远还不到饱暖思淫欲的时刻，中国人很多时候还是在想如何在淘宝赚钱，或者说更多人还停留在网址导航，停留在打开电脑只看qq的年代。
#我一直坚信的是，facebook和twitter打通了一条信息的流动的通路，但是通往信息最终散落的地方的很多重要的，有价值的内容其实并没有 得到完全的承载。因此如果说前一阵（5年左右时间）的大事情是信息的传播，社会化的话，我相信在一段时间过去最大的价值是各种有价值的信息的承载和细分。
#这些细分已经逐渐的显现出来了。包括，音乐类Spotify。问答类Quora。旅行类daodao等等。在一段时间内的细分市场会更加垂直和深入，以不同的方式展示和聚合最有价值的部分信息，真正为社会化的网络搭建的这条信息通道输送内容。
#那下一个是Pinterest吗？它能不能在中国顺利的成长？我觉得借鉴一下delicious的经验就可以知道这是很难的一条路，yupoo也没有完全复制Flickr的成功。或许或许，在中国Pinterest的机会不在花瓣，而在于美丽说。    
#'''
#    topic_rank = defaultdict(float)
#    idf = idf_zhihu()
#    tfidf_list = sorted(idf.tf_idf(txt), key=lambda x:x[1], reverse=True)
#
#    for word, tfidf in tfidf_list:
#        print "-",word,tfidf
#    print ''
#    for word_tfidf, word_id in zip(
#        [i[1] for i in tfidf_list],
#        WORD2ID.id_list_by_word_list(i[0] for i in tfidf_list)
#    ):
#        if word_id in BAYES_RANK:
#            for topic_id, bayes in BAYES_RANK[word_id]:
#                topic_rank[topic_id] += (word_tfidf*bayes)
#
#    topic_rank = sorted(topic_rank.iteritems(), key=lambda x:x[1], reverse=True)
#    for topic_id, rank in topic_rank:
#        print ID2TAG[topic_id], rank
