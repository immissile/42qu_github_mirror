# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.po import Po
from model.po_video import po_video_new
from model.zsite_tag import zsite_tag_new_by_tag_id
from model.cid import CID_VIDEO
from model.state import STATE_ACTIVE

@urlmap('/po/video')
@urlmap('/po/video/(\d+)')
class PoVideo(LoginBase):
    def post(self, po_id=0):
        cid = CID_VIDEO
        video_url = self.get_argument('video', None)
        name = self.get_argument('name', None)
        txt = self.get_argument('txt', None)


        link = '/live'

        if po_id:
            po_id = int(po_id)
            po = Po.mc_get(po_id)
            if po and po.user_id == self.current_user_id:
                po.name_ = name
                po.txt_set(txt)
                po.save()
                link = po.link
        else:
            video = self._video(video_url)
            if video:
                user_id = self.current_user_id
                po = po_video_new(user_id, name, txt, video, STATE_ACTIVE)
                if po:
                    po_id = po.id

                    link = '/po/tag/%s' % po_id


        return self.redirect(link)

    def _video(self, video_url):
        if video_url.startswith('http://v.youku.com/v_show/id_'):
            video = video_url[29:42]
        elif video_url.startswith('http://player.youku.com/player.php/sid/'):
            video = video_url[39:52]
        if video.isalnum() and len(video) == 13:
            return video

