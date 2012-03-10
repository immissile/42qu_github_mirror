#coding:utf-8

from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, McCacheA
from model.cid import CID_STAR
from model.zsite import zsite_new
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

class ZsiteStar(Model):
    pass

def star_ico_new(user_id, pic):
    from model.ico import site_ico_new
    return site_ico_new(user_id, pic)

def zsite_star_new(
    user_id, name,  txt, donate_min, end_days, pic_id
):
    from model.ico import site_ico_bind
    zsite = zsite_new(name, CID_STAR)
    id = zsite.id
    txt_new(id, txt)
    zs = ZsiteStar(
        id = id,
        donate_min = donate_min,
        po_id = 0,
        end_days = end_days
    )
    zs.save()
    site_id = zs.id
    site_ico_bind(user_id, pic_id, site_id)
    return zsite

if __name__ == "__main__":
    pass



