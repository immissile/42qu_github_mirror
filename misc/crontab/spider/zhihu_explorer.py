# -*- coding: utf-8 -*-

import _env
from yajl import loads
from zkit.htm2txt import htm2txt
import urllib2
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
import  time
from writer import Spider

def fetch(url, headers):
    if not headers:
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
                'Accept': ' text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
                'Accept-Language':'zh-cn,zh;q=0.5',
                'Accept-Charset':'gb18030,utf-8;q=0.7,*;q=0.7',
                'Content-type':'application/x-www-form-urlencoded'
                }

    request = urllib2.Request(
            url,
            headers=headers
            )
    urlopener = urllib2.build_opener()
    r = urlopener.open(request)

    j = r.read()

    return j

def page_fetch(id, headers=None):
    url = 'http://www.zhihu.com/question/%s'%id
    return fetch(url, headers)

def main():
    cookies = (
            ('b3179509@nwldx.com', '_xsrf=7ed86e897bae4b9e8cf3e660efed7baf; q_c0=MTk2OTAzfGdmWDM5Q2pZNVpaUW9UTzA=|1326267926|eedfe70f85add0db0ecda1e73200cac9b085ecc6; __utma=155987696.1247389772.1322703824.1326190947.1326266591.29; __utmb=155987696.34.10.1326266591; __utmc=155987696; __utmz=155987696.1325768571.27.6.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=155987696.Logged%20In'),
            )

    headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Language':'en,en-US;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'www.zhihu.com',
            'Referer:http':'//www.zhihu.com/',
            'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
            }
    count = 0
    headers['cookie'] = cookies[0][1]
    explore_page = fetch('http://www.zhihu.com/explore', headers=headers)


    entry_list = txt_wrap_by_all('<div class="xxn">', '</div', explore_page)
    reting_raw = txt_wrap_by("['explore_list',", ');', explore_page)
    data = loads(reting_raw)
    author_list = [[i[3][1][0].encode('utf-8'), i[3][2].encode('utf-8')] for i in data]
    rating_list = [i[3][3] for i in data]

    label_list = txt_wrap_by_all('"padding:3px 0 0" class="xm">', '</div', explore_page)
    result_label = [txt_wrap_by_all('">', '</a', i) for i in label_list]


    url_list = txt_wrap_by_all('<h2', '</h2>', explore_page)
    id_list = [txt_wrap_by('question/', '/answer', i) for i in url_list]
    title_list = [txt_wrap_by('">', '<', txt_wrap_by('href="', '/a>', i))for i in url_list]

    url_list = txt_wrap_by_all('<h2', '</h2>', explore_page)
    id_list = [txt_wrap_by('question/', '/answer', i) for i in url_list]
    url_list = ['http://www.zhihu.com/question/%s'%id for id in id_list]

    entry_list = zip(title_list, rating_list, result_label, author_list, url_list, entry_list)

    for entry in entry_list:
        content, pic_list = htm2txt(entry[5])
        Spider.insert(entry[0], entry[2], content, entry[3][0], entry[1] , entry[4], [], pic_list)



if __name__ == '__main__':
    main()
