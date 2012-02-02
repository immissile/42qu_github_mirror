# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from model.zsite_site import zsite_id_by_zsite_user_id
from ctrl._urlmap.zsite import urlmap
from model.state import STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
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

        link = '/feed'

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
                zsite_id = zsite_id_by_zsite_user_id(self.zsite, user_id)

                if zsite_id:
                    state = STATE_PO_ZSITE_SHOW_THEN_REVIEW
                else:
                    state = STATE_ACTIVE

                po = po_audio_new(
                    user_id, name, txt, audio,
                    state,
                    zsite_id=zsite_id
                )

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



