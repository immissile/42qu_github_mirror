# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.po import Po
from model.po_audio import po_audio_new
from model.zsite_tag import zsite_tag_new_by_tag_id
from model.cid import CID_AUDIO

@urlmap('/po/audio')
@urlmap('/po/audio/(\d+)')
class PoAudio(LoginBase):
    def post(self, po_id=0):
        cid = CID_AUDIO
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
                link = '/po/tag/%s' % po_id
        else:
            audio = self._audio()
            if audio:
                user_id = self.current_user_id
                po = po_audio_new(user_id, name, txt, audio)
                if po:
                    po_id = po.id
                    link = '/po/tag/%s' % po_id

        return self.redirect(link)

    def _audio(self):
        files = self.request.files
        audio = files.get('audio')
        if audio:
            audio = audio[0]['body']
            if not audio:
                return
            if not (len(audio) > 1024*1024*512):
                return audio



