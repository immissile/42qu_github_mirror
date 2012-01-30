#coding:utf-8

import _env
from zkit.spider import Rolling, Fetch, NoCacheFetch, GSpider

#Cookie: bid="55/9+SIFH50"; __gads=ID=227c583a14c13dc1:T=1327909678:S=ALNI_MaHgWBFQ_WaU31RNei_UaAIoRXb0Q; dbcl2="1262808:PQFaR3yY2cI"; ck="O91t"; __utma=30149280.1492613719.1327909685.1327909685.1327909685.1; __utmb=30149280.2.10.1327909685; __utmc=30149280; __utmz=30149280.1327909685.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=30149280.126

def spider(url_list):
    headers = {
        'Cookie': 'bid="i9gsK/lU40A"; ll="108288"; __gads=ID=94ec68b017d7ed73:T=1324993947:S=ALNI_MaYLBDGa57C4diSiOVJspHn0IAVQw; __utma=164037162.1587489682.1327387877.1327387877.1327387877.1; __utmz=164037162.1327387877.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); viewed="7153184"; __utmb=164037162.2.8.1327387877; __utmc=164037162; RT=s=1327387895075&r=http%3A%2F%2Fwww.douban.com%2Fnote%2F196951541%2F; dbcl2="13593891:UKKGQFylj18"; ck="lLgF"'

    }
    #headers = {}
    fetcher = NoCacheFetch( headers=headers)
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=1, debug=debug)
    spider_runner.start()


