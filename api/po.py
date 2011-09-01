#!/usr/bin/env python
#coding:utf-8
import _handler
from _urlmap import urlmap
from model.po import po_word_new, Po, po_rm
from model.zsite import user_can_reply, Zsite
from model import reply
from model.po_video import po_video_new, VIDEO_CID_YOUKU, VIDEO_CID_TUDOU, VIDEO_CID_SINA
from model.cid import CID_VIDEO, CID_PHOTO, CID_AUDIO
from model.zsite_tag import zsite_tag_new_by_tag_id
from model.po_photo import po_photo_new
from model.state import STATE_ACTIVE
from zkit.pic import picopen
from model.po_audio import po_audio_new
from model.zsite_tag import zsite_tag_new_by_tag_id, zsite_tag_new_by_tag_name

@urlmap('/po/word')
class PoWord(_handler.OauthAccessBase):
    def get(self):
        user_id = self.current_user_id
        txt = self.get_argument('txt')
        result = {}
        if txt.strip():
            m = po_word_new(user_id, txt)
            if m:
                result['id'] = m.id
                result['link'] = 'http:%s'%m.link
        self.finish(result)


@urlmap('/po')
class PoAll(_handler.OauthAccessBase):
    def get(self):
        user_id = self.current_user_id
        po_id = int(self.get_argument('id'))
        po = Po.mc_get(po_id)
        itr = []
        if po.user_id == user_id:
            for reply in po.reply_list():
                re = {}
                re['id'] = reply.id
                re['user_id'] = reply.user.id
                re['user_name'] = reply.user.name
                re['txt'] = reply.txt
                re['timestamp'] = reply.create_time
                itr.append(re)
        self.finish({
                'items':itr
            })


@urlmap('/po/rm')
class PoRm(_handler.OauthAccessBase):
    def get(self):
        id = int(self.get_argument('id'))
        user = self.current_user
        user_id = self.current_user_id
        m = po_rm(user_id, id)
        self.finish({
                'status':m
            })


@urlmap('/po/reply')
class PoReply(_handler.OauthAccessBase):
    def get(self):
        id = int(self.get_argument('id'))
        po = Po.mc_get(id)
        m = None
        if po:
            user = self.current_user
            if user_can_reply(user):
                user_id = self.current_user_id
                can_view = po.can_view(user_id)
                link = po.link_reply
                if can_view:
                    txt = self.get_argument('txt', '')
                    m = po.reply_new(user, txt, po.state)
        self.finish({
                'id' : m
            })


@urlmap('/po/reply/rm')
class PoReplyRm(_handler.OauthAccessBase):
    def get(self):
        id = int(self.get_argument('id'))
        user_id = self.current_user_id
        r = reply.Reply.mc_get(id)
        can_rm = None
        if r:
            po = Po.mc_get(r.rid)
            if po:
                can_rm = r.can_rm(user_id) or po.can_admin(user_id)
                if can_rm:
                    r.rm()
        self.finish({'status': can_rm})

@urlmap('/po/video')
class PoVideo(_handler.OauthAccessBase):
    def get(self):
        po_id = int(self.get_argument('id',0))
        cid = CID_VIDEO
        url = self.get_argument('video', None)
        name = self.get_argument('name', None)
        txt = self.get_argument('txt', None)


        if po_id:
            po_id = int(po_id)
            po = Po.mc_get(po_id)
            if po and po.user_id == self.current_user_id:
                po.name_ = name
                po.txt_set(txt)
                po.save()
        else:
            if url:
                video, video_site = self._video(url)
                if video:
                    user_id = self.current_user_id
                    po = po_video_new(user_id, name, txt, video, video_site)
                    if po:
                        po_id = po.id

        current_user = self.current_user
        current_user_id = self.current_user_id
        po = Po.mc_get(po_id)
        if not po.can_admin(current_user_id):
            return self.finish({'error':'cant admin'})
        if po:
            tag_id = int(self.get_argument('tag',0))
            name = self.get_argument('tag_name', None)

            if not name and not tag_id:
                tag_id = 1

            if tag_id:
                zsite_tag_new_by_tag_id(po, tag_id)
            else:
                zsite_tag_new_by_tag_name(po, name)

        return self.finish({'link':'http:%s'%po.link,'id':po.id})

    def _video(self, url):
        if url.startswith('http://v.youku.com/v_show/id_'):
            video = url[29:url.rfind('.')]
            video_site = VIDEO_CID_YOUKU
        elif url.startswith('http://player.youku.com/player.php/sid/'):
            video = url[39:url.find("/",39)]
            video_site = VIDEO_CID_YOUKU
        elif url.startswith('http://www.tudou.com/programs/view/'):
            video = url[35:].rstrip("/")
            video_site = VIDEO_CID_TUDOU
        elif url.startswith('http://video.sina.com.cn/v/b/'):
            video = url[29:url.rfind('.')]
            video_site = VIDEO_CID_SINA
        else:
            video = None
            video_site = None
        return video, video_site


@urlmap('/po/photo')
class PoPhoto(_handler.OauthAccessBase):
    def post(self):
        cid = CID_PHOTO
        po_id = int(self.get_argument('id',0))

        name = self.get_argument('name', None)
        txt = self.get_argument('txt', None)

        

        if po_id:
            po_id = int(po_id)
            po = Po.mc_get(po_id) 
            if po and po.user_id == self.current_user_id:
                po.name_ = name
                po.txt_set(txt)
                po.save()
        else:
            img = self._img()
            if img:
                user_id = self.current_user_id
                po = po_photo_new(user_id, name, txt, img, STATE_ACTIVE)
                po_id = po.id


        current_user = self.current_user
        current_user_id = self.current_user_id
        po = Po.mc_get(po_id)

        if po:
            if not po.can_admin(current_user_id):
                return self.finish({'error':'cant admin'})
            tag_id = int(self.get_argument('tag',0))
            name = self.get_argument('tag_name', None)

            if not name and not tag_id:
                tag_id = 1

            if tag_id:
                zsite_tag_new_by_tag_id(po, tag_id)
            else:
                zsite_tag_new_by_tag_name(po, name)

            return self.finish({'link':'http:%s'%po.link,'id':po.id})

        
    def _img(self):
        files = self.request.files
        img = files.get('photo')
        if img:
            img = img[0]['body']
            if not len(img) > 1024*1024*12:
                img = picopen(img)
                if not img:
                    return
                return img


@urlmap('/po/audio')
class PoAudio(_handler.OauthAccessBase):
    def post(self):
        cid = CID_AUDIO
        po_id = int(self.get_argument('id',0))
        name = self.get_argument('name', None)
        txt = self.get_argument('txt', None)
        

        if po_id:
            po_id = int(po_id)
            po = Po.mc_get(po_id) 
            if po and po.user_id == self.current_user_id:
                po.name_ = name
                po.txt_set(txt)
                po.save()
        else:
            audio = self._audio()
            if audio:
                user_id = self.current_user_id
                po = po_audio_new(user_id, name, txt, audio)
                if po:
                    po_id = po.id

        current_user = self.current_user
        current_user_id = self.current_user_id
        po = Po.mc_get(po_id)
        if po:
            if not po.can_admin(current_user_id):
                return self.finish({'error':'cant admin'})
            tag_id = int(self.get_argument('tag',0))
            name = self.get_argument('tag_name', None)

            if not name and not tag_id:
                tag_id = 1

            if tag_id:
                zsite_tag_new_by_tag_id(po, tag_id)
            else:
                zsite_tag_new_by_tag_name(po, name)

        return self.finish({'link':'http:%s'%po.link,'id':po.id})

        
    def _audio(self):
        files = self.request.files
        audio = files.get('audio')
        if audio:
            audio = audio[0]['body']
            if not audio:
                return
            if not (len(audio) > 1024*1024*512):
                return audio


