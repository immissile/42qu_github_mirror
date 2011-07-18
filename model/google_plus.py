#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from time import time
from zkit.bot_txt import txt_wrap_by

#GOOGLE_PLUS_URL_PROXY = 'http://gplus.com/%s/about?hl=zh-CN'
GOOGLE_PLUS_URL = 'https://plus.google.com/%s/about?hl=zh-CN'
GOOGLE_PLUS_URL_PROXY = GOOGLE_PLUS_URL
#'http://gplus.com/%s/about?hl=zh-CN'

class GoogleRank(McModel):
    @property
    def follower_rank(self):
        return self.where('follower>%s', self.follower).count()+1


def google_rank_by_uid(uid):
    return GoogleRank.get(uid=uid)

def google_rank_new(uid, follower, ico, name, txt):
    rank = GoogleRank.get_or_create(uid=uid)
    rank.follower = follower
    rank.ico = ico
    rank.name = name
    rank.txt = txt
    rank.update_time = time()
    rank.save()
    return rank

def google_rank_new_by_html(uid, html):
    jpg = txt_wrap_by(
        'height="200" src="//',
        'photo.jpg?sz=200',
        html
    )
    jpg = '//%sphoto.jpg'%jpg #?sz=200

    follower = txt_wrap_by(
        '（',
        '）',
        txt_wrap_by(
            '>圈子中有', '</h4>', html
        )
    )
    if follower:
        follower = follower.replace(',', '')
        if not follower.isdigit():
            follower = 0
    else:
        follower = 0
    name = txt_wrap_by('<title>', '</title>', html).rsplit(' - ')[0]
    txt = txt_wrap_by(
            """介绍</h2><div """,
            '''</div></div><div class="''',
            html
        )
    if txt:
        txt = txt[txt.find('note">')+6:].replace('</div>', ' ').replace('<div>', ' ').replace('<span>', '').replace('</span>', '').strip()
    return google_rank_new(uid, follower, jpg, name, txt)

def google_uid_by_link(uid):
    uid = uid.strip()
    if '://' in uid:
        uid = uid[uid.find('://')+3:].split('/', 2)[1]
    return uid


if __name__ == '__main__':
    from urllib2 import urlopen
    url = 'https://plus.google.com/%s/about?hl=zh-CN'
    id = '107234826207633309420'
    html = urlopen(url%id).read()
    google_rank_new_by_html(id, html)

    for id in GoogleRank.where().order_by('follower desc').col_list(None, None, 'uid'):
        print id
        try:
            html = urlopen(url%id).read()
        except:
            print id
            continue
        google_rank_new_by_html(id, html)

# follower = txt_wrap_by(
#     "（",
#     "）",
#     txt_wrap_by(
#         '>圈子中有', '</h4>', html
#     )
# )
# print follower
#
#    txt = txt_wrap_by(
#        '>',
#        '<',
#        txt_wrap_by(
#            """介绍</h2><div """,
#            """/div>""",
#            html
#        )
#    )
#    career = txt_wrap_by(
#            """工作经历</h2><div """,
#            """</ul>""",
#            html
#        )
#    career = career[career.find('<ul '):]+'</ul>'
#
#    marry = txt_wrap_by(
#        '>',
#        '<',
#        txt_wrap_by(
#            """婚恋</h2><div """,
#            """/div>""",
#            html
#        )
#    )
#    sex = txt_wrap_by(
#        '>',
#        '<',
#        txt_wrap_by(
#            """性别</h2><div """,
#            """/div>""",
#            html
#        )
#    )
#    name = txt_wrap_by('<title>', '</title>', html).rsplit(' - ')[0]

#  print txt
#  print career
#  print marry
#  print sex
