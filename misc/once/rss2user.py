#!/usr/bin/env python
#coding:utf-8
import _env
import re
from model.rss import Rss
from model.zsite import Zsite

RE_LINK = re.compile(
r'((?:https?://[\w\-]+\.)'
r'[\w\-.%/=+#:~!,\'\*\^@]+'
r'(?:\?[\w\-.%/=+#:~!,\'\*&$@]*)?)'
)
def get_url():
    with open('substring.txt') as string:
        url = []
        for i in string.readlines():
            i.strip()
            x = RE_LINK.findall(i)
            if x:
                url.append(x[0])
        return url


def LongestCommonSubstring(S1, S2):
    M = [[0]*(1+len(S2)) for i in xrange(1+len(S1))]
    longest, x_longest = 0, 0
    for x in xrange(1,1+len(S1)):
        for y in xrange(1,1+len(S2)):
            if S1[x-1] == S2[y-1]:
                M[x][y] = M[x-1][y-1] + 1
                if M[x][y]>longest:
                    longest = M[x][y]
                    x_longest  = x
            else:
                M[x][y] = 0
    return S1[x_longest-longest: x_longest]

def get_x():
    with open('rss2user_id.txt') as string:
        urls = []
        for i in string.readlines():
            i = i.strip().split()
            urls.append(i)
        return urls

if __name__ == "__main__":
    x = get_x()
    rss = Rss.where()
    userdict = {}
    rss_id2user_id = {}
    for r in rss:
        if Zsite.mc_get(r.user_id) and Zsite.mc_get(r.user_id).cid ==1:
            max_id,max_num = 0,0
            for i,j in enumerate(x):
                l = len(LongestCommonSubstring(r.link,j[1]))
                if max_num < l:
                    max_num = l
                    max_id = i
            #print x[max_id][1],r.id
            #r.link = x[max_id][1]
            if r.user_id in userdict  or max_num<7:
                print '!!!!!!!',max_num,r.user_id,x[max_id][1]
            else:
                rss_id2user_id[r.id] = r.user_id



