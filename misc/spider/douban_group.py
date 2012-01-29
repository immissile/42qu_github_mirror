#coding:utf-8
import _env
from model.douban import DoubanGroup, DoubanFeedOwner, DoubanFeed, CID_DOUBAN_FEED_TOPIC

class ParseGroupHtm(object):
    def member_num(self, data):
        return txt_wrap_by('浏览所有成员 (', ')', data)

    def group_id(self, data):
        tmp = txt_wrap_by('<form action="/group/topic_search', '</form', data)
        return txt_wrap_by('<input type="hidden" value="', '" name="group', tmp)

    def group_short_url(self, data):
        return txt_wrap_by('http://www.douban.com/feed/group/' , '/discussion', data)

    def leader_id(self, data):
        t = txt_wrap_by('组长：', '</a>', data)
        return txt_wrap_by('www.douban.com/people/', '/">', data)

    def title(self, data):
        return txt_wrap_by('<title>', '</title>', data).strip()

    def intro(self, data):
        t = txt_wrap_by('class="infobox">', '<div class="rec-sec', data.replace('\r', ' ').replace('\n', ' '))
        return txt_wrap_by('</p>', ' <div', t)

    def __call__(self, data, url):
        member_num = self.member_num(data)
        group_id = self.group_id(data)
        leader_id = self.leader_id(data)
        title = self.title(data)
        intro = self.intro(data)
        short_url = self.group_short_url(data)

        group = DoubanGroup.new(group_id, url, name)
        
        group.url = 


        return member_num, group_id, short_url, leader_id, title, intro

parse_group_htm = ParseGroupHtm()

if __name__ == '__main__':
    pass
    from zweb.orm import ormiter
    exist = set()
    for i in ormiter(DoubanFeedOwner):
        feed = DoubanFeed.get(i.id)
        if feed.cid == CID_DOUBAN_FEED_TOPIC:
            group_url = feed.rid or i.topic
            group = DoubanGroup.by_url(group_url)
            if not group:
                if not group_url in exist:
                    exist.add(group_url)
                    yield parse_group_htm, "http://www.douban.com/group/%s/"%group_url
            else:
                print group.name



