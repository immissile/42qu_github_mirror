#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model.feed_import import feed2po_new, zsite_id_by_douban_user_id, FeedImport, IMPORT_FEED_STATE_INIT, DOUBAN_ZSITE_ID, IMPORT_FEED_CID_DICT
from model.duplicate import Duplicator
from zkit.txt import format_txt
from config import DUMPLICATE_DB_PREFIX
from zkit.htm2txt import htm2txt
from model.douban import douban_feed_to_review_iter, DoubanUser
from zkit.single_process import single_process
from zkit.classification.classification import GetTag

tag_getter = GetTag()

douban_duplicator = Duplicator(DUMPLICATE_DB_PREFIX%'douban')

def feed_import_by_douban_feed():
#    count = 0
    for i in douban_feed_to_review_iter():
#        if count> 10:
#            break
#        count+=1
#        print "!"
        feed_import_new(
            i.title, i.htm, i.link, i.id, DOUBAN_ZSITE_ID
        )

def feed_import_new(title, txt, url, src_id, zsite_id, tags='', state=IMPORT_FEED_STATE_INIT):
    txt = format_txt(htm2txt(txt)).replace('豆友', '网友').replace('豆油', '私信').replace('豆邮', '私信')
    if not douban_duplicator.txt_is_duplicate(txt):

        # douban_user = DoubanUser.get(author_id)
        # user_id = zsite_id_by_douban_user_id(douban_user)

        #cid = IMPORT_FEED_CID_DICT[zsite_id]

        if not tags:
            tags = '`'.join(tag_getter.get_tag(txt))

        new_feed = FeedImport(
                title=title,
                txt=txt,
                zsite_id=zsite_id,
                state=state,
                rid=src_id,
                url=url,
                tags=tags,
                )

        new_feed.save()
        douban_duplicator.set_record(txt, new_feed.id)

        return new_feed


@single_process
def main():
    #feed2po_new()
    feed_import_by_douban_feed()


if __name__ == '__main__':
    #main()
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
    print  tag_getter.get_tag(txt)
