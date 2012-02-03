#coding:utf-8
import _env
from urllib import urlencode
from model.netease_photo import netease_user_new, netease_photo_new, netease_album_new
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from zkit.htm2txt import htm2txt, unescape

#起始点
PHOTO_163_URL = 'http://pp.163.com/pp'

#c0-param0:栏目(column)id,(人像,婚纱,风景...) ,p=10,40...
#c0-param1:翻页起始图片id，第一个从0开始，第二个从18开始,page=1,2...
#co-param2:返回的图片数目,默认是18
PHOTO_163_NEWLIST_URL = 'http://photo.163.com/share/dwr/call/plaincall/PictureSetBean.getPictureSetNewListByDirId.dwr?callCount=1&scriptSessionId=%24%7BscriptSessionId%7D187&c0-scriptName=PictureSetBean&c0-methodName=getPictureSetNewListByDirId&c0-id=0&c0-param0=number%3A{0}&c0-param1=number%3A{1}&c0-param2=number%3A18&batchId=483816'

PHOTO_NUM_PER_PAGE = 18

#某作者的一个作品集
PHOTO_163_ALBUM_URL = 'http://photo.163.com/{0}/pp/{1}.html'

#要获取点击数，得post到这个地址
PHOTO_163_HITS_POST_URL = 'http://photo.163.com/share/dwr/call/plaincall/PicSetInteractionBean.getLikeViewCount.dwr'

#点击数在这个以下的图片不要
HITS_THRESHOLD = 100

def build_hits_req(photos):
    req = {}
    req['url'] = PHOTO_163_HITS_POST_URL
    data = []
    data.append('callCount=1')
    data.append('scriptSessionId=${scriptSessionId}187')
    data.append('c0-scriptName=PicSetInteractionBean')
    data.append('c0-methodName=getLikeViewCount')
    data.append('c0-id=0')
    num = len(photos)
    for i in range(num):
        data.append('c0-e%s=number:%s' % (str(i+1), str(photos[i][2])))

    content = ','.join('reference:c0-e%s'%(i+1) for i in xrange(num) )
    data.append('c0-param0=Array:[%s]' % content)

    for i in range(num):
        data.append('c0-e%s=number:%s' %
                    (str(num+i+1), str(photos[i][1])))

    content = ','.join('reference:c0-e%s'%(i+1+num) for i in xrange(num) )
    data.append('c0-param1=Array:[%s]' % content)
    data.append('batchId=204172')

    req['data'] = '\n'.join(data)
    return req

def photo_163_parse_photo_album(data, url, u_name, a_id, u_id, hits):
    #返回 标题, 作者名字, 作者id , 拍摄地点 ,拍摄时间, 图片的网址列表
    #163的页面用的是gbk编码
    data = data.decode('gbk').encode('utf-8')
    title = txt_wrap_by(" name: '", "',", data)
    author = txt_wrap_by("nickName : '"
                    , "',", data)
    author_url = txt_wrap_by("hostHomeUrl :'", "',", data)
    place = txt_wrap_by('拍摄于 </span>', '<b class=', data)
    place = place.replace('<em>', '').replace('</em>', '')
    published = txt_wrap_by('发布于 </span>', '</h6>', data).strip()
    print '\n', url
    print ' | '.join([title, published, author, author_url, place, hits, u_id,
                   u_name, a_id])

    user = netease_user_new(u_id, author_url, author, u_name)
    album = netease_album_new(user, title, u_id, place, published, url)
    for img in txt_wrap_by_all('<div class="picnt">', '</div>', data):
        src = txt_wrap_by('data-lazyload-src="', '"', img)
        if src is None:
            src = txt_wrap_by(' src="', '"', img)
        netease_photo_new(src, album)
        print src

def photo_163_parse_hits(data, url, photo_list):
    for i in range(len(photo_list)):
        photo_list[i].append(txt_wrap_by('s'+str(i)+'.vcnt=', ';', data))
    photo_list = filter(lambda e:int(e[3])>HITS_THRESHOLD, photo_list)
    for u_name, u_id, a_id, hits in photo_list:
        album_url = PHOTO_163_ALBUM_URL.format(u_name, a_id)
        #print u_name, u_id, a_id, hits ,album_url
        yield photo_163_parse_photo_album, album_url, u_name, a_id, u_id, hits

def photo_163_parse_column_newlist(data, url, column_id, page_num):
    print '\n',url, '\t', column_id,'\t', page_num
    photo_list = []
    photo_ids = txt_wrap_by_all('var ', '={}', data)
    for i in photo_ids:
        user_name = txt_wrap_by(i+'.domainName=', ';', data)
        if 'null' == user_name:
            user_name = txt_wrap_by(i+'.uname=', ';', data)
        user_name = user_name.strip('"')
        album_id = txt_wrap_by(i+'.id=', ';', data)
        user_id = txt_wrap_by(i+'.aopUserId=', ';', data)
        photo_list.append([user_name, user_id, album_id])

    yield photo_163_parse_hits, build_hits_req(photo_list), photo_list

    if len(photo_ids) == PHOTO_NUM_PER_PAGE:
        yield photo_163_parse_column_newlist,\
                PHOTO_163_NEWLIST_URL.\
                    format(column_id, (page_num+1)*PHOTO_NUM_PER_PAGE), column_id, page_num+1

def photo_163_parse_main(data, url):
    for column_id in txt_wrap_by_all('sid="', '"><span', data):
        yield photo_163_parse_column_newlist,\
                 PHOTO_163_NEWLIST_URL.format(column_id, '0'), column_id, 0


from zkit.spider import Rolling, Fetch, MultiHeadersFetch, NoCacheFetch, GSpider
def spider(url_list):
    fetcher = NoCacheFetch()
    spider = Rolling( fetcher, url_list )
    spider_runner = GSpider(spider)
    spider_runner.start()

def main():
    url_list = []
    url_list.append((photo_163_parse_main, PHOTO_163_URL))
    spider(url_list)

if __name__ == '__main__':
    main()
