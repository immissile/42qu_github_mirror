#coding:utf-8
import _env
from config import FS_URL

VIDEO_CID_YOUKU = 1
VIDEO_CID_TUDOU = 2
VIDEO_CID_SINA = 3
VIDEO_CID_SLIDESHARE = 4

LINK_AUTOPLAY_YOUKU = 'http://static.youku.com/v/swf/qplayer.swf?VideoIDS=%s=&isShowRelatedVideo=false&showAd=0&winType=interior&isAutoPlay=true'

LINK_AUTOPLAY_TUDOU = 'http://www.tudou.com/v/%s&autoPlay=true/v.swf'

LINK_AUTOPLAY_SINA = 'http://p.you.video.sina.com.cn/swf/quotePlayer20110627_V4_4_41_20.swf?autoplay=1&vid=%s&uid=%s'

LINK_SLIDESHARE = '%s/swf/ssplayer2.swf?doc=%%s&rel=0'%FS_URL

LINK_YOUKU = 'http://static.youku.com/v/swf/qplayer.swf?VideoIDS=%s=&isShowRelatedVideo=false&showAd=0&winType=interior'


LINK_TUDOU = 'http://www.tudou.com/v/%s/v.swf'


LINK_SINA = 'http://p.you.video.sina.com.cn/swf/quotePlayer20110627_V4_4_41_20.swf?vid=%s&uid=%s&autoPlay=0'

_HTM_SWF = '''<embed src="%s" quality="high" class="video" allowfullscreen="true" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash" wmode= "Opaque"></embed>'''

VIDEO_CID2LINK = {
    VIDEO_CID_YOUKU      :  LINK_YOUKU,
    VIDEO_CID_TUDOU      :  LINK_TUDOU,
    VIDEO_CID_SINA       :  LINK_SINA,
    VIDEO_CID_SLIDESHARE :  LINK_SLIDESHARE,
}

VIDEO_CID2LINK_AUTOPLAY = {
    VIDEO_CID_YOUKU      :  LINK_AUTOPLAY_YOUKU,
    VIDEO_CID_TUDOU      :  LINK_AUTOPLAY_TUDOU,
    VIDEO_CID_SINA       :  LINK_AUTOPLAY_SINA,
    VIDEO_CID_SLIDESHARE :  LINK_SLIDESHARE,
}


def video_filter(url):
    if url.startswith('http://v.youku.com/v_show/id_'):
        video = url[29:url.rfind('.')]
        video_site = VIDEO_CID_YOUKU
    elif url.startswith('http://player.youku.com/player.php/sid/'):
        video = url[39:url.find('/', 39)]
        video_site = VIDEO_CID_YOUKU
    elif url.startswith('http://www.tudou.com/programs/view/'):
        video = url[35:].rstrip('/')
        video_site = VIDEO_CID_TUDOU
    elif url.startswith('http://video.sina.com.cn/v/b/'):
        video = url[29:url.rfind('.')]
        video_site = VIDEO_CID_SINA
    elif url.startswith('http://static.slidesharecdn.com/swf/ssplayer2.swf?'):
        begin = url.find('doc=')+4
        video = url[begin:url.find('&', begin)]
        video_site = VIDEO_CID_SLIDESHARE
    else:
        video = None
        video_site = None
    return video, video_site


def video_autoplay_link(url , link_dict=VIDEO_CID2LINK):
    video , video_site = video_filter(url)

    if video_site is None:
        return

    return video_link_by_cid_uri(video_site, video, VIDEO_CID2LINK_AUTOPLAY)

def video_link_by_cid_uri(cid, uri, link_dict=VIDEO_CID2LINK):
    if cid == VIDEO_CID_SINA:
        uri = tuple(uri).split('-')
    return link_dict[cid]%uri

if __name__ == '__main__':
    pass
    print video_autoplay_link('http://v.youku.com/v_show/id_XMzE4MDI5NjI4.html')


