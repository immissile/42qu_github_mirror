#coding:utf-8
from model.po_pic import pic_list, mc_pic_id_list
from model.po_pic import pic_can_add, po_pic_new, po_pic_rm
from model.po import Po, CID_WORD, CID_NOTE
from zkit.pic import picopen
from model.fs import fs_url_jpg
from json import dumps

def _pic_upload(self, user_id, po_id):
    files = self.request.files
    img = files.get('img')
    if img:
        img = img[0]['body']
    else:
        return 0


    if len(img) > 1024*1024*12:
        return 2

    img = picopen(img)
    if not img:
        return 10

    if po_id:
        po = Po.mc_get(po_id)
        if not po or po.user_id != user_id or (po.cid == CID_WORD and po.rid == 0):
            return 0
        if po.cid == CID_WORD:
            from model.po_question import answer_word2note
            answer_word2note(po)

    if not pic_can_add(user_id, po_id):
        return 16

    pic = po_pic_new(user_id, po_id, img)
    if not pic:
        return 14

    r = {
        'status': 0,
        'src': fs_url_jpg(219, pic.id),
        'seqid': pic.seq,
    }
    return r

def pic_upload(self, user_id, po_id=0):
    if po_id:
        po_id = int(po_id)

    r = _pic_upload(self, user_id, po_id)
    if isinstance(r, (int, long)):
        r = {'status':r}
    #USE DUMPS FIX HEADER FOR FIREFOX
    r = dumps(r)
    self.finish(r)

def pic_upload_rm(self, user_id, po_id):
    seq = self.get_argument('seq')
    po_pic_rm(user_id, po_id, seq)
    self.finish('{}')

def update_pic(form, user_id, po_id, id):
    pl = pic_list(user_id, id)
    for pic in pl:
        seq = pic.seq

        title = 'tit%s' % seq
        if title in form:
            title = form[title][0]
        else:
            title = ''

        align = 'pos%s' % seq
        if align in form:
            align = int(form[align][0])
            if align not in (-1, 0, 1):
                align = 0
        else:
            align = 0

        pic.title = title.strip()
        align = int(align)


        pic.align = align
        pic.po_id = po_id
        pic.save()

    mc_pic_id_list.delete(
        '%s_%s' % (user_id, id)
    )

if __name__ == "__main__":
    pass



