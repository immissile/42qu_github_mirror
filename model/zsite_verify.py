#coding:utf-8
from _db import Model
from zsite import Zsite, ZSITE_STATE_ACTIVE, ZSITE_STATE_VERIFY, \
CID_USER,  ZSITE_STATE_FAILED_VERIFY
from model.ico import ico
from model.career import career_current
from model.zsite_show import zsite_show_rm

ZSITE_VERIFY_NEED_NAME     = 0b1
ZSITE_VERIFY_NEED_ICO      = 0b10
ZSITE_VERIFY_NEED_CAREER   = 0b100

#CREATE TABLE `zpage`.`zsite_user_verifyed` (
#  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
#  `user_id` INTEGER UNSIGNED NOT NULL,
#  `state` INTEGER UNSIGNED NOT NULL,
#  PRIMARY KEY (`id`),
#  INDEX `Index_2`(`user_id`)
#)
#ENGINE = MyISAM;
ZSITE_USER_VERIFYED_UNCHECK = 1
ZSITE_USER_VERIFYED_CHECKED = 2

class ZsiteUserVerifyed(Model):
    pass

def zsite_verify_rm(zsite):
    zsite.state = ZSITE_STATE_FAILED_VERIFY
    zsite.save()
    zsite_show_rm(zsite)

def zsite_verify_new(zsite):
    if zsite.state >= ZSITE_STATE_VERIFY:
        return

    zsite.state = ZSITE_STATE_VERIFY
    zsite.save()

    user_id = zsite.id
    if ZsiteUserVerifyed.get(user_id=user_id, state=ZSITE_USER_VERIFYED_UNCHECK):
        return

    v = ZsiteUserVerifyed(user_id=user_id, state=ZSITE_USER_VERIFYED_UNCHECK)
    v.save()


def zsite_verify_ajust(zsite):
    if zsite.cid != CID_USER:
        return

    need = 0
    id = zsite.id

    if zsite.name.isdigit():
        need |= ZSITE_VERIFY_NEED_NAME 

    if not ico.get(id):
        need |= ZSITE_VERIFY_NEED_ICO 
    
    if not any(career_current(id)):
        need |= ZSITE_VERIFY_NEED_CAREER
 
    if need:
        zsite_verify_rm(zsite)
        return need
    else: 
        zsite_verify_new(zsite)

if __name__ == '__main__':

    from zweb.orm import ormiter
    for zsite in ormiter(
        Zsite,
        'state>=%s and state<%s and cid=%s'%(
            ZSITE_STATE_ACTIVE, ZSITE_STATE_VERIFY, CID_USER
        )
    ):
        print zsite.id, zsite_verify_ajust(zsite)
        
