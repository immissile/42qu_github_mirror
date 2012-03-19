import urllib2
from urllib import urlencode
from json import loads
import _env
from zkit.bot_txt import txt_wrap_by_all
from xml.sax.saxutils import unescape
from time import sleep

def read_next(start, offset):
    data = {
        'offset':offset,
        'start':start
    }
    result = []
    data = urlencode(data)
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'Accept': ' text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
               'Accept-Language':'zh-cn,zh;q=0.5',
               'Accept-Charset':'gb18030,utf-8;q=0.7,*;q=0.7',
               'Content-type':'application/x-www-form-urlencoded'
            }


    headers['Cookie'] = """__utma=155987696.1466564421.1323058814.1323081063.1323082137.3; __utmz=155987696.1323082137.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=site%3Azhihu.com; __utmv=155987696.Logged%20In; _xsrf=5f0d189d485b43cca16068abe2d981ec; __utmc=155987696; __utmb=155987696.70.10.1323082137; checkcode=d3Nsag==|1323081329|606c2864ea806947dae5b5a8d7ab17c2ad22894e; q_c0=MTY2MzIxfFZHUkQxQ2xweUp6Y1czMDk=|1323083404|aabdf01be80a6e1b1c2f6817b03ef2de8a62eb2f"""

    request = urllib2.Request(
        url='http://www.zhihu.com/log/questions',
        data=data,
        headers=headers
    )
    urlopener = urllib2.build_opener()
    r = urlopener.open(request)

    j = r.read()
    j = loads(j)
    html = j['msg'][1]

    name_list = txt_wrap_by_all('''</h2>

<div>

<a''', '<', html)

    id_list = txt_wrap_by_all('logitem-' , '">', html)
    begin = '<a href="/question/'
    end = '</a'
    for id, name, i in zip(id_list, name_list, txt_wrap_by_all(begin, end, html)):
        i = i.split('">', 1)
        i.append(id)
        name = unescape(name).strip()[14:].split('">', 1)
        if len(name) < 2:
            name = '?', '?'
        i.extend(name)
        result.append(i)

    return 20+offset, result


def main():
    #start = 9937205
    #start = 7084667
    start = 7085090
    offset = 0
    while True:
        offset, result = read_next(start, offset)
        if not result:
            break
        start = int(result[-1][2])
        for i in result:
            print i[2], i[0], i[3], i[4].replace(' ', '_'), unescape(i[1]).replace('\r', ' ').replace('\n', ' ')

        sleep(1)

if __name__ == '__main__':
    main()
