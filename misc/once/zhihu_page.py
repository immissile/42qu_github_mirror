import urllib2
import _env
from time import sleep
from os.path import exists

def page_fetch(id):
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
               'Accept': ' text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
               'Accept-Language':'zh-cn,zh;q=0.5',
               'Accept-Charset':'gb18030,utf-8;q=0.7,*;q=0.7',
               'Content-type':'application/x-www-form-urlencoded'
            }


    headers['Cookie'] = """__utma=155987696.1466564421.1323058814.1323081063.1323082137.3; __utmz=155987696.1323082137.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=site%3Azhihu.com; __utmv=155987696.Logged%20In; _xsrf=5f0d189d485b43cca16068abe2d981ec; __utmc=155987696; __utmb=155987696.70.10.1323082137; checkcode=d3Nsag==|1323081329|606c2864ea806947dae5b5a8d7ab17c2ad22894e; q_c0=MTY2MzIxfFZHUkQxQ2xweUp6Y1czMDk=|1323083404|aabdf01be80a6e1b1c2f6817b03ef2de8a62eb2f"""

    request = urllib2.Request(
        url='http://www.zhihu.com/question/%s'%id,
        headers=headers
    )
    urlopener = urllib2.build_opener()
    r = urlopener.open(request)

    j = r.read()

    return j


def main():
    count = 0
    with open('zhihu.txt') as zhihu:
        for line in zhihu:
            line = line.strip().split(' ', 2)
            id = line[1]
            if id.isdigit():
                count += 1
                print line[0], count
                path = 'zhihu/%s.html'%id
                if exists(path):
                    continue
                try:
                    html = page_fetch(id)
                except:
                    continue
                with open(path, 'w') as zhihu:
                    zhihu.write(html)
            sleep(.5)

if __name__ == '__main__':
    main()
