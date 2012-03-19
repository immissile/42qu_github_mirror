#coding:utf-8

import _env
from zkit.spider import Rolling, MultiHeadersFetch, GSpider

COOKIE = (
    'bid="i9gsK/lU40A"; ll="108288"; __gads=ID=94ec68b017d7ed73:T=1324993947:S=ALNI_MaYLBDGa57C4diSiOVJspHn0IAVQw; __utma=164037162.1587489682.1327387877.1327387877.1327387877.1; __utmz=164037162.1327387877.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); viewed="7153184"; __utmb=164037162.2.8.1327387877; __utmc=164037162; RT=s=1327387895075&r=http%3A%2F%2Fwww.douban.com%2Fnote%2F196951541%2F; dbcl2="13593891:UKKGQFylj18"; ck="lLgF"',
    'bid="Mksh/jzha94"; __gads=ID=a97391d1ff39e159:T=1327963852:S=ALNI_Mb3JwOj--ZmKyyfxJK3KCnZ0FC42A; dbcl2="58152412:1wJ9EMDfj+4"; ck="y4k4"; __utma=30149280.58903610.1327963887.1327963887.1327963887.1; __utmb=30149280.4.10.1327963887; __utmc=30149280; __utmz=30149280.1327963887.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=30149280.5815'  ,
    'bid="nEgHvgAsWEE"; __gads=ID=2b98e7952a634985:T=1327963957:S=ALNI_MZB-OBrqBqdnaoPwjRPUcSaMXGCtQ; dbcl2="2071563:+uSySLuPTDw"; ck="crbf"; __utma=30149280.294517378.1327963985.1327963985.1327963985.1; __utmb=30149280.4.10.1327963985; __utmc=30149280; __utmz=30149280.1327963985.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=30149280.207' ,
    'bid="AD1wrRA/Clc"; __gads=ID=f963176c5ef49907:T=1327964066:S=ALNI_MZ10_yq5XmQI1jkKGr-2lxMfyVcQg; ll="None"; __utma=30149280.1335466508.1327964087.1327964087.1327964087.1; __utmb=30149280.8.9.1327964120431; __utmc=30149280; __utmz=30149280.1327964087.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dbcl2="4370980:FrK9jGcZRvg"; ck="ZrnT"; __utmv=30149280.437',
    'bid="gXkh1+2pD1Q"; __gads=ID=159f5a09680a102a:T=1327964159:S=ALNI_MZED-MqF7s6_IBt0RP7xJyJVOoBoA; __utma=30149280.191617523.1327965175.1327965175.1327965175.1; __utmb=30149280.5.9.1327965176225; __utmc=30149280; __utmz=30149280.1327965133.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); RT=s=1327965183472&r=https%3A%2F%2Fwww.douban.com%2Faccounts%2Fresetpassword%3Fconfirmation%3D740009460988b488; dbcl2="34007358:tEe97AUZqSs"; ck="beqN"; __utmv=30149280.3400'
)

def spider(url_list):
    fetcher = MultiHeadersFetch( 
        headers=tuple(
            { 'Cookie': i } for i in COOKIE
        )
    )
    spider = Rolling( fetcher, url_list )

    debug = False
    debug = True

    spider_runner = GSpider(spider, workers_count=2, debug=debug)
    spider_runner.start()


