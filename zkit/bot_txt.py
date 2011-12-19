#coding:utf-8
import re
def txt_wrap_by(begin, end, html):
    if not html:
        return ''
    start = html.find(begin)
    if start >= 0:
        start += len(begin)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def txt_wrap_by_all(begin, end, html):
    if not html:
        return ''
    result = []
    from_pos = 0
    while True:
        start = html.find(begin, from_pos)
        if start >= 0:
            start += len(begin)
            endpos = html.find(end, start)
            if endpos >= 0:
                result.append(html[start:endpos].strip())
                from_pos = endpos+len(end)
                continue
        break
    return result

def strip_line(txt):
    if not txt:
        return ''
    txt = txt.replace('　', ' ').split('\n')
    return '\n'.join(i for i in [i.strip() for i in txt] if i)

def strip_txt_wrap_by(begin, end, html):
    if not html:
        return ''
    t = txt_wrap_by(begin, end, html)
    if t:
        return strip_line(t)


def txt_map(begin_string, end_string, html, func):
    txt = []
    result = []
    prepos = None
    preend = 0
    len_end_string = len(end_string)
    len_begin_string = len(begin_string)
    while True:
        if prepos is None:
            pos = html.find(begin_string)
        else:
            pos = html.find(begin_string, prepos)
        if pos >= 0:
            end = html.find(end_string, pos)
        if pos < 0 or end < 0:
            result.append(html[preend:])
            break
        end = end+len_end_string
        result.append(html[preend:pos])
        tmp = func(html[pos:end])
        if tmp:
            result.append(tmp)
        prepos = pos+len_begin_string
        preend = end

    return ''.join(result)


if __name__ == '__main__':
    pass
    xml = """

{{{
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE wml PUBLIC "-//WAPFORUM//DTD WML 1.1//EN" " http://www.wapforum.org/DTD/wml_1.1.xml"> <wml> <head> <meta http-equiv="Cache-Control" content="max-age=0" /> <meta http-equiv="Cache-control" content="no-cache" /> <meta name="robots" content="noindex" /> </head> <card title="3GQQ聊天-手机腾讯网"> <p> </p> <p><a href=" http://q16.3g.qq.com/g/s?new3gqq=true&amp;aid=nqqchatMain&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;3G_UIN=316293191&amp;saveURL=0"><img src=" http://221.204.186.50/qbar/qbar_qqui_online.gif" alt="聊天"/>QQ</a><a href=" http://info.z.qq.com/infocenter_v2.jsp?g_f=6437&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;3G_UIN=316293191&amp;saveURL=0&amp;B_UID=316293191&amp;fc=0"><img src=" http://221.204.186.50/qbar/qbar_qinfo_0.gif" alt="空间"/>(0)</a><a href=" http://ti2.3g.qq.com/g/s?aid=h&amp;g_f=5407&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;3G_UIN=316293191&amp;saveURL=0"><img src=" http://221.204.186.50/qbar/qbar_microblog_home.gif" alt="微博"/>(0)</a><a href=" http://wap.wenwen.soso.com/mybox.jsp?g_f=1870&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;3G_UIN=316293191&amp;saveURL=0"><img src=" http://221.204.186.50/qbar/qbar_wenwen_1.gif" alt="问问"/>(0)</a><a href=" http://qbar.3g.qq.com/g/qbar/qbar_list.jsp?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;3G_UIN=316293191&amp;saveURL=0">&gt;&gt;</a></p><p align="left"> <a href=" http://sqq.3g.qq.com/s?aid=go&amp;pgId=3gnews_prepay&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;bi=1_24_0_-1_55&amp;g_redirect_url=http%3A%2F%2Fsqq%2E3g%2Eqq%2Ecom%2Fact%2F201111cft%2Findex%2Ejsp%3Fg%5Ff%3D12321&amp;amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt">[特]充超级QQ赢iPad</a><br/> 【QQ好友】(<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqStatus">上线</a>)<br/> 在线|<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqRecent">最近</a>|<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqchatMain&amp;on=0&amp;g_f=1655">离线</a>|<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqGroup">分组</a>|<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=app_list">应用</a>|<a href=" http://sqq.3g.qq.com/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=bizp&amp;pt=act&amp;pc=3gqqgroup">群</a><br/> <a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqchatMain&amp;on=1">手动刷新</a>.<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqAutoRefSettingIntro">自动刷新</a> <br/> <a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqChat&amp;u=919923309&amp;on=1&amp;g_f=1660"><img src=" http://119.167.195.52/images/face/newonline/130-1.gif" alt="."/>邓尘</a> <br/> <a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqChat&amp;u=736770240&amp;on=1&amp;g_f=1660"><img src=" http://119.167.195.52/images/face/newleave/1-1.gif" alt="."/>杨柳</a> <br/> <a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqChat&amp;u=2424110056&amp;on=1&amp;g_f=1660"><img src=" http://119.167.195.52/images/face/newonline/1-1.gif" alt="."/>゛〆呆子°</a> <br/> <a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqchatMain&amp;on=1&amp;p=1">上页</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqchatMain&amp;on=1&amp;p=2">下页</a><br/> 第2/2页<br/> <input name="searchKey" type="text" size="3"/> <select name="searchType" multiple="false" value="1" > <option value="1">按昵称</option> <option value="2">按备注</option> <option value="3">按号码</option> </select> <anchor>搜好友 <go href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=localSearch" method="post"> <postfield name="searchKey" value="$searchKey"/> <postfield name="searchType" value="$searchType"/> </go> </anchor><br/> 【QQ辅助】<br/> <a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqSelf">设置</a>.<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=find">查找</a>.<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=logout&amp;from=logout">更改用户</a><br/> <a href=" http://lt4.3g.qq.com/g/topic_list.jsp?forumId=1497&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt">论坛</a>.<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=logout">退出</a> .<a href=" http://wap.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=wapsupport&amp;fid=435">问题反馈</a><br/> 聊3GQQ时还可以:<br/> <a href=" http://blog60.z.qq.com/index_real.jsp?3g_sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;g_f=9336">空间</a>.<a href=" http://app.qq.com/g/s?aid=new_category&amp;time=true&amp;cid=120&amp;g_f=990035&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;g_ut=1">游戏</a>.<a href=" http://ebook12.3g.qq.com/?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;g_f=9335&amp;aid=book">书城</a>.<a href=" http://music.wap.soso.com/search.jsp?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;from=3gqq&amp;g_f=6009">搜歌</a>.<a href=" http://ti.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;g_f=2586&amp;aid=h">微博</a><br/> <a href=" http://sqq.3g.qq.com/index.jsp?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;g_f=1295">超Q</a>.<a href=" http://m.paipai.com/g/s?aid=index&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;g_f=5136&amp;g_ut=1">购物</a>.<a href=" http://novel.wap.soso.com/search.jsp?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=index&amp;g_f=5272&amp;biz=3gqq_novel">搜书</a>.<a href=" http://house60.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=home_self&amp;g_f=9334">家园</a>.<a href=" http://pet.3g.qq.com/index.jsp?g_f=1232&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt">宠物</a><br/> <br/> <input name="searchSoSo" type="text" size="6"/> <anchor>搜搜 <go href=" http://wap.soso.com/s.q?type=sweb&amp;st=input&amp;g_f=2938&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;biz=3gqq" method="post"> <postfield name="key" value="$searchSoSo"/> </go> </anchor><br/> <a href=" http://wap.3g.qq.com/g/s?aid=adp_click&amp;ad_s=L&amp;pid=75&amp;adid=64647&amp;adpid=51776&amp;adactid=51515&amp;go=http%3A%2F%2Fmisc.3g.qq.com%2Fg%2Fs%3Faid%3Dtemplate%26tid%3Dbqdx%26g_f%3D5925%26sid%3DAeaVqmCXlSnZeEzPOYSq0iRt&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt">让美眉心跳不已的短信,发了吗</a><br/><a href=" http://wap.3g.qq.com/g/s?aid=adp_click&amp;ad_s=L&amp;pid=140&amp;adid=64831&amp;adpid=52119&amp;adactid=51858&amp;go=http%3A%2F%2Fapp.qq.com%2Fg%2Fs%3Faid%3Ddetail%26productId%3D23226%26g_f%3D7644%26sid%3DAeaVqmCXlSnZeEzPOYSq0iRt&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt">老同学新同事都在这里等你</a><br/><a href=" http://wap.3g.qq.com/g/s?aid=adp_click&amp;ad_s=L&amp;pid=142&amp;adid=50373&amp;adpid=52161&amp;adactid=51900&amp;go=http%3A%2F%2Fmg.3g.qq.com%2Flogin.jsp%3Fcpid%3D916%26gameid%3D126%26cid%3D3g%26sid%3DAeaVqmCXlSnZeEzPOYSq0iRt&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt">[英雄]而过回眸一笑群芳失色</a><br/> </p> <p> 普通版|<a href=" http://q32.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nqqGroup&amp;g_f=1657&amp;g_ut=2&amp;gutswicher=2">3G版</a> <br/> <a href=" http://info50.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=index&amp;login=false">手机腾讯网</a>-<a href=" http://info50.3g.qq.com/g/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=navigation">导航</a>-<a href=" http://app.qq.com/g/?g_f=990281&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt">软件</a>-<a href=" http://pt5.3g.qq.com/s?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;aid=nLogout">退出</a><br /><a href=" http://info60.z.qq.com/infocenter_v2.jsp?g_f=6438&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;3G_UIN=316293191&amp;saveURL=0">空间(0)</a>.<a href=" http://house3.3g.qq.com/g/s?aid=home_self&amp;g_f=595&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;3G_UIN=316293191&amp;saveURL=0">家园(0)</a>.<a href=" http://ti2.3g.qq.com/g/s?aid=h&amp;g_f=6439&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;3G_UIN=316293191&amp;saveURL=0">微博(0)</a><br /><a href=" http://wap.soso.com/navi.jsp?sid=AeaVqmCXlSnZeEzPOYSq0iRt&amp;g_f=6228">搜搜</a><input name="key" type="text" value="诈骗3亿"/><anchor><go href=" http://wap.soso.com/sweb/search.jsp?st=input&amp;g_f=6215&amp;sid=AeaVqmCXlSnZeEzPOYSq0iRt" method="post"><postfield name="key" 
}}}
value="$key"/></go>搜网页</anchor><br />小Q报时(14:35)<br /></p> </card> </wml>
【提示：此用户正在使用Q+ Web： http://web.qq.com/】 """


    def replace_code(match):
        return '12345'
    RE_CODE = re.compile(r'\{\{\{(.*?)\}\}\}', re.S)

    def test_re():
        s = RE_CODE.sub(replace_code, xml)
    def test_map():
        s = txt_map('{{{', '}}}', xml, replace_code)

    import timeit
    t = timeit.Timer('test_re()', 'from __main__ import test_re')
    print t.timeit(10000)

    t = timeit.Timer('test_map()', 'from __main__ import test_map')
    print t.timeit(10000)
