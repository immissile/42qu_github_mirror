#coding:utf-8

import _env
from collections import defaultdict
from zkit.idf import idf_zhihu
from mmseg import seg_txt
from yajl import loads
from generate_lib import TAG2ID, WORD2ID, BAYES_RANK
from zkit.txt_cleanup import sp_txt

import sys;
reload(sys);
sys.setdefaultencoding('utf-8')

ID2TAG = TAG2ID.id2word()

class GetTag(object):
    def __init__(self ):
        self.idf = idf_zhihu()

    def get_tag(self, txt):
        topic_rank = defaultdict(float)
        tfidf_list = sorted(self.idf.tf_idf(txt), key=lambda x:x[1], reverse=True)

        highest_word_list = []
        for word, tfidf in tfidf_list[:10]:
            if word in ID2TAG.values():
                highest_word_list.append(TAG2ID.id_by_tag(word))

        for word_tfidf, word_id in zip(
            [i[1] for i in tfidf_list],
            WORD2ID.id_list_by_word_list(i[0] for i in tfidf_list)
        ):
            if word_id in BAYES_RANK:
                for topic_id, bayes in BAYES_RANK[word_id]:
                    topic_rank[topic_id] += (word_tfidf*bayes)

        topic_rank = sorted(topic_rank.iteritems(), key=lambda x:x[1], reverse=True)

        for topic_id, rank in topic_rank[:10]:
            '''
            推荐主题做二元分词, 如果文章中没有, 则去掉. 
            '''
            for seg in sp_txt(ID2TAG[topic_id]):
                if seg in txt:
                    #print seg
                    yield ID2TAG[topic_id]
                    break

                

        #for k in highest_word_list:
        #    print ID2TAG[k]

        #return highest_word_list
        #return ','.join([ID2TAG[k] for k in highest_word_list])


if __name__ == '__main__':
    txt = '''
辞旧迎新之际，匆匆把一年来在豆瓣所写的日志翻看了一遍，不免有些惊讶，虎年日志有四十多篇，自己已然觉得颇不少了，兔年所写日志竟有五十多篇，有朋友责怪我于此不甚积极，看来好像是不公之论，我的日志信息量比较大、图片比较多，哪怕是摘抄选录，也比较花费时间，无法多写或为情理中事，假如有人不满意，也只能说抱歉，我想我已尽力了，抛砖引玉也好，自露乖丑也罢，这里照例列一个纲目索引。

这一年来图影游记不少，自己看了之后，都会有种这人一直到处乱跑的印象，文字不足道，我也实在没有心力详细解说，只是自己的备录，假如有二三友邻以此作为应目会心的卧游，我就觉得大欣慰了。

寅秋辽京津狂奔图影录之义县[[http://www.douban.com/note/134811216/]]  推荐 46人 35人喜欢

庚寅秋辽京津狂奔图影录之帝都[[http://www.douban.com/note/140903751/]]  推荐 20人 20人喜欢

庚寅秋辽京津狂奔图影录之蓟县天津[[http://www.douban.com/note/145956644/]]  推荐 56人 53人喜欢

辛卯年立春晋东南行记之第一篇——高平[[http://www.douban.com/note/158882716/]]  推荐 65人 80人喜欢

辛卯年立春晋东南行记之第二篇——泽州[[http://www.douban.com/note/159066768/]]  推荐 79人 90人喜欢

辛卯年立春晋东南行记之第三篇——晋城[[http://www.douban.com/note/159678736/]]  推荐 138人 134人喜欢

辛卯年立春晋东南行记之完结篇——沁县[[http://www.douban.com/note/160063714/]]  推荐 83人 81人喜欢

辛卯年春分川蜀行记之第一篇——绵阳[[http://www.douban.com/note/161037133/]]  推荐 102人 108人喜欢

辛卯年春分川蜀行记之第二篇——阆中[[http://www.douban.com/note/162051772/]]  推荐 45人 44人喜欢

辛卯年春分川蜀行记之第三篇——巴中[[http://www.douban.com/note/162447858/]]  推荐 71人 71人喜欢

辛卯年春分川蜀行记之第四篇——广元[[http://www.douban.com/note/163669799/]]  推荐 59人 61人喜欢

辛卯年立夏定州高碑店帝都行记[[http://www.douban.com/note/169698598/]]  推荐 50人 51人喜欢

辛卯年夏至陕甘行之天水麦积山[[http://www.douban.com/note/174969781/]]  推荐 197人 219人喜欢

辛卯年夏至陕甘行之甘肃武山[[http://www.douban.com/note/176910894/]]  推荐 324人 359人喜欢

辛卯年夏至陕甘行之甘肃甘谷[[http://www.douban.com/note/178325426/]]  推荐 48人 50人喜欢

辛卯年夏至陕甘行之陕西宝鸡[[http://www.douban.com/note/178539709/]]  推荐 54人 52人喜欢

辛卯年夏至陕甘行之西安碑林石刻[[http://www.douban.com/note/178962177/]]  推荐 115人 131人喜欢

辛卯年夏至陕甘行之西安一夜[[http://www.douban.com/note/179729431/]]  推荐 63人 57人喜欢

辛卯年夏至陕甘行之陕西彬县大佛寺[[http://www.douban.com/note/180369921/]]  推荐 48人 50人喜欢

辛卯年夏至陕甘行之完结篇南京大云山汉墓[[http://www.douban.com/note/182070960/]]  推荐 130人 45人喜欢

虽然多是图影流水，不过去年在结缘豆篇中所列的规划，如南京、成都两地的游记，都大致完成了，从推荐数量上来看，似乎不算是应付之作，也有不少朋友喜欢，我自然也高兴。

庚寅冬扬州南京散步图影录之扬州篇[[http://www.douban.com/note/147661488/]]  推荐 256人 247人喜欢

《金陵再记》小引——哭梧桐[[http://www.douban.com/note/152496223/]]  推荐 55人 57人喜欢

金陵漫记图影录（上）[[http://www.douban.com/note/153374900/]]  推荐 354人 386人喜欢

金陵漫记图影录（下）[[http://www.douban.com/note/157106865/]]  推荐 235人 263人喜欢

辛卯年春分川蜀行记之完结篇——成都[[http://www.douban.com/note/167335833/]]  推荐 297人 326人喜欢

自己稍觉遗憾的是，《太行游记》系列一年里只完成了两篇，而这两篇还是去年已准备好的，原因我想大概是因为这系列接下来的篇什都与中国古建筑有关，如隆兴寺、南禅寺、佛光寺、应县塔、善化寺等等，基础不夯实的话，内容自然难免泛泛，龙年专心于此，或能有多写几篇。

太行内外行记之二十——赵县柏林寺[[http://www.douban.com/note/185601479/]]  推荐 32人 14人喜欢

太行内外行记之二十一 —— 赵县陀罗尼经幢[[http://www.douban.com/note/187312264/]]  推荐 72人 32人喜欢

兔年所写日志中，最受友邻欢迎的是本朱讲文物历史考古方面的日志，尤其是说北朝文物和有关日本三篇，不虞之誉和求全之毁，这方面我也不想多说了，总之还是老话，这是外行人的不自量力地胡扯八道，观者当多有警惕以免上当！

八音——从考古文物看中国乐器（上）[[http://www.douban.com/note/136499887/]]  推荐 155人 146人喜欢

八音——从考古文物看中国乐器（下）[[http://www.douban.com/note/136512569/]]  推荐 86人 82人喜欢

说说良渚玉器、琮、钺及其他[[http://www.douban.com/note/164930205/]]  推荐 332人 434人喜欢

抄书笔记之“说说木桥”[[http://www.douban.com/note/172183159/]]  推荐 113人 133人喜欢

融汇与贯通——那个牛逼闪闪的时代！[[http://www.douban.com/note/173205707/]]  推荐 450人 582人喜欢

美丽的日本——文物历史篇[[http://www.douban.com/note/139776571/]]  推荐 1199人 1175人喜欢

美丽的日本——东瀛建筑篇[[http://www.douban.com/note/196560384/]]  推荐 1220人 1228人喜欢

美丽的日本——信仰寺庙篇[[http://www.douban.com/note/144879161/]]  推荐 571人 587人喜欢

书还是胡乱地买，尤其是新书，近年买得实在不能算少了，已经好多年未有这样买书，不知是喜是忧。

辛卯初春所见所得[[http://www.douban.com/note/142394142/]]  推荐 38人 34人喜欢

偶的419收获（有图有真相！！！）[[http://www.douban.com/note/146358415/]]  推荐 130人 120人喜欢

革命老区起义日所得书目[[http://www.douban.com/note/152877522/]]  推荐 39人 41人喜欢

朱头斋存书图影录之戏曲篇（上）[[http://www.douban.com/note/150075302/]]  推荐 74人 72人喜欢

那一瞥幽怨的眼神——近期得书书影志（上）[[http://www.douban.com/note/165801431/]]  推荐 126人 144人喜欢

那一瞥幽怨的眼神——近期得书书影志（下）[[http://www.douban.com/note/170791524/]]  推荐 15人 16人喜欢

辛卯中秋得书录[[http://www.douban.com/note/174793023/]]  推荐 11人 12人喜欢

关于《陈寅恪文集》及其他[[http://www.douban.com/note/181156285/]]  推荐 103人 52人喜欢

近期所得新书谈（书影版）[[http://www.douban.com/note/184443152/]]  推荐 71人 34人喜欢

近期所得新书续谈（书影版）[[http://www.douban.com/note/184613007/]]  推荐 69人 28人喜欢

近期所得新书三谈（书影版）[[http://www.douban.com/note/187738802/]]  推荐 85人 39人喜欢

重在参与旧书谈（近期所购旧书书影志）[[http://www.douban.com/note/190254424/]]  推荐 29人 19人喜欢

11年末旧书懒谈（佛教美术类）[[http://www.douban.com/note/192819678/]]  推荐 41人 17人喜欢

11年岁末新书书影录（上）[[http://www.douban.com/note/193932051/]]  推荐 48人 19人喜欢

唐风宋雨祝新年[[http://www.douban.com/note/194177397/]]  推荐 517人 426人喜欢

兔年并没有参加社会活动，日志里只有到义乌去膜拜碗帝一篇。

富春山水记及义乌围观碗帝记[[http://www.douban.com/note/148899128/]]  推荐 47人 44人喜欢

其他的都是杂项类，其中印度小数点单位及刘起釪先生晚景凄凉两篇本是转载加工之作，不想引起了不小的议论和评说且多方转载，印度数字单位篇自当忽略，可又是一年，现在还有哪位关心刘先生呢？！

朱头败家录（兼及吃喝）稀释盐咸！！馋虫馋鬼和半夜老饿者绝对慎入！！！[[http://www.douban.com/note/137798745/]]   推荐 22人 20人喜欢

这样的夏天过去了！！[[http://www.douban.com/note/174592879/]]  推荐 32人 32人喜欢

遥知兄弟登高处[[http://www.douban.com/note/176199689/]]  推荐 87人 95人喜欢

中国古代的大小数单位名称（印度阿三不是人！！！）[[http://www.douban.com/note/151137991/]]  推荐 1814人 1809人喜欢

几年来最让我震惊的报道——著名先秦史學家、尚書學家、古史辨派——刘起釪先生晚年淒涼[[http://www.douban.com/note/135189419/]]  推荐 5109人 4702人喜欢

想写点感旧录，无奈此类难言，只有一篇，十三章的规划看来将遥遥无期了。

感旧十三章之“儿时”[[http://www.douban.com/note/153986543/]]  推荐 114人 125人喜欢

在去年的“关于长夜”篇中，我曾引知堂的话代言心声，这里再重录于下：

“我自己写文章是属于哪一派的呢？说兼爱固然够不上，为我也未必然，似乎这里有点儿缠夹，而结缘的豆乃仿佛似之，岂不奇哉。写文章本来是为自己，但他同时要一个看的对手，这就不能完全与人无关系，盖写文章即是不甘寂寞，无论怎样写得难懂意识里也总期待有第二人读，不过对于他没有过大的要求，即不必要他来做喽罗而已。煮豆微撒以盐而给人吃之，岂必要索厚偿，来生以百豆报我，但只愿有此微末情分，相见时好生看待，不至伥伥来去耳。”

这一年来所发日志每篇都有友邻推荐和喜欢，此刻查看，最少的推荐数的日志也有11人推荐，或说明至少有11位友邻抬举，这又何尝不是好生看待，本朱不至伥伥来去耳？！希望前辈高人继续给予点拨指正的，彼此在新年里都多多有所进步！在这里也恭祝各位师友身体健康！！万事如意！！

'''
    cla = GetTag()
    print ','.join(cla.get_tag(txt))
    raw_input()
    print ','.join(cla.get_tag(txt))
    print ','.join(cla.get_tag(txt))
    print ','.join(cla.get_tag(txt))
    print ','.join(cla.get_tag(txt))
    print ','.join(cla.get_tag(txt))

#ID2TAG = TAG2ID.id2word()
#
#if __name__ == '__main__':
#
#    txt = '''
#Pinterest的一些思考 #周末在家的时候，除了重构了部分代码以外，最多的时候想的就是Pinterest这件事情。最近太多关关于Pinterest的新闻出来了，包括花瓣拿到的4.5 M 美金的投资。包括估值巨高的Pinterest的各种事情。
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
