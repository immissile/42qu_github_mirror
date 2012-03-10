#coding:utf-8

from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, McCacheA
from model.cid import CID_STAR
from model.zsite import zsite_new, Zsite
from model.txt import txt_new

#CREATE TABLE `zpage`.`zsite_star` (
#  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
#  `donate_min` INTEGER UNSIGNED NOT NULL,
#  `donate_now` INTEGER UNSIGNED NOT NULL DEFAULT 0,
#  `end_time` INTEGER UNSIGNED NOT NULL,
#  `po_id` INTEGER UNSIGNED NOT NULL,
#  PRIMARY KEY (`id`)
#)
#ENGINE = MyISAM;

class ZsiteStar(McModel):
    @property
    def pic_id(self):
        from model.ico import ico96 
        return ico96.get(self.id)

    def can_admin(self, user_id):
        return self.user_id == user_id
    
def star_ico_new(user_id, pic):
    from model.ico import site_ico_new
    return site_ico_new(user_id, pic)

def zsite_star_new(
    user_id, name,  txt, donate_min, end_days, pic_id
):
    zsite = zsite_new(name, CID_STAR)
    id = zsite.id
    txt_new(id, txt)
    zs = ZsiteStar(
        id = id,
        donate_min = donate_min,
        po_id = 0,
        user_id = user_id,
        end_days = end_days
    )
    zs.save()
    site_id = zs.id
    star_pic_bind(user_id, pic_id, id)
    return zsite

def star_pic_bind(user_id, pic_id, id):
    from model.ico import site_ico_bind
    site_ico_bind(user_id, pic_id, id)


def zsite_star_get(id):
    zsite = Zsite.mc_get(id)
    if not zsite or zsite.cid != CID_STAR:
        return
    zsite.star = ZsiteStar.mc_get(id)
    return zsite
#
#def po_note_new_for_zsite_star(user_id, name, txt, state=STATE_ACTIVE, zsite_id=0):
#    pass

from model.po import po_new, CID_NOTE, STATE_ACTIVE

def zsite_star_po_note_new(id, name, txt):
    if not name and not txt:
        return
    po = po_new( CID_NOTE, id, name, STATE_ACTIVE )
    if po:
        po.txt_set(txt)
        return po



if __name__ == "__main__":
    pass



