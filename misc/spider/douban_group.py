#coding:utf-8
import _env
from model.douban import DoubanGroup, DoubanFeedOwner, DoubanFeed, CID_DOUBAN_FEED_TOPIC, DoubanUser
from zkit.bot_txt import txt_wrap_by
from zkit.htm2txt import htm2txt, unescape

class ParseGroupHtm(object):
    def member_num(self, data):
        #女巫店小组 浏览所有店里的小孩们 (43025
        line = txt_wrap_by('/members">', ')</a>', data)
        if not line:
            return 0
        return int(txt_wrap_by(' (', None, line))

    def group_id(self, data):
        tmp = txt_wrap_by('<form action="/group/topic_search', '</form', data)
        return txt_wrap_by('<input type="hidden" value="', '" name="group', tmp)

    def group_short_url(self, data):
        return txt_wrap_by('http://www.douban.com/feed/group/' , '/discussion', data)

    def leader_id(self, data):
        t = txt_wrap_by('组长：', '</a>', data)
        return txt_wrap_by('www.douban.com/people/', '/">', data) or 0

    def name(self, data):
        return unescape(str(txt_wrap_by('<title>', '</title>', data).strip())[:-6]) #xxx小组

    def intro(self, data):
        t = txt_wrap_by('class="infobox">', '<div class="rec-sec', data.replace('\r', ' ').replace('\n', ' '))
        return txt_wrap_by('</p>', ' <div', t)

    def __call__(self, data, url):
        member_num = self.member_num(data)
        group_id = self.group_id(data)
        leader_id = self.leader_id(data)
        name = self.name(data)
        intro = self.intro(data)
        short_url = self.group_short_url(data)

        print name, member_num, leader_id

        group = DoubanGroup.new(group_id, short_url, name)
        group.member = member_num
        group.leader = leader_id
        group.save()


parse_group_htm = ParseGroupHtm()

def main():
    from zweb.orm import ormiter
    exist = set()
    for i in ormiter(DoubanFeedOwner):
        topic_id = None
        user_id = None

        feed = DoubanFeed.get(i.id)
        if feed.cid == CID_DOUBAN_FEED_TOPIC:
            group_url = feed.topic_id or i.topic
            group = DoubanGroup.by_url(group_url)
            if not group:
                if not group_url in exist:
                    exist.add(group_url)
                    yield parse_group_htm, 'http://www.douban.com/group/%s/'%group_url

            else:
                topic_id = group

        user_id = feed.user_id or i.owner
        if not (user_id and str(user_id).isdigit()): 
            user_id = DoubanUser.by_url(user_id)
        
        if topic_id is not None and user_id:
            feed.topic_id = topic_id
            feed.user_id = user_id
            feed.save()
            i.delete()


if __name__ == '__main__':
    pass

    from douban_spider import  spider

    spider(main())


