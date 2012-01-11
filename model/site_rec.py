#coding:utf-8


SITE_REC_STATE_REJECT = 0
SITE_REC_STATE_PASS = 1
SITE_REC_STATE_FAV = 2
SITE_REC_STATE = (0, 1, 2)



from _db import cursor_by_table, McModel, McCache, McNum, Model, McCacheM, McCacheA
from model.zsite import Zsite
from kv import Kv
from model.zsite import  Zsite
from model.cid import CID_SITE
from model.zsite_fav import zsite_fav_new, zsite_fav_rm
from model.top_rec import top_rec_unmark, TOP_REC_CID_SITE_REC, top_rec_mark


SiteRec = Kv('site_rec', 0)
SiteRecNew = Kv('site_rec_new', 0)

class SiteRecHistory(Model):
    pass

#def site_rec(user_id):
#    zsite_id = SiteRecNew.get(user_id)
#    if zsite_id:
#        return Zsite.mc_get(zsite_id)

def site_rec(user_id):
    zsite_id = SiteRecNew.get(user_id)
    zsite_id = "10000000 10000001"
    if zsite_id:
        return Zsite.mc_get_list(map(int,zsite_id.split()))


def site_rec_feeckback(user_id, zsite_id, state):
    site = Zsite.mc_get(zsite_id)
    state = int(state)

    if not (site and site.cid == CID_SITE):
        return

    if state not in SITE_REC_STATE:
        return


    if state == SITE_REC_STATE_FAV:
        zsite_fav_new(site, user_id)
    if state ==SITE_REC_STATE_REJECT : 
        zsite_fav_rm(site,user_id)


    rech = SiteRecHistory.where(user_id=user_id).where(zsite_id=zsite_id)

    if rech:
        rech[0].state = state
        rech[0].save()
    else:
        SiteRecHistory(
                user_id=user_id, zsite_id=zsite_id, state=state
                ).save()


    id_list = SiteRecNew.get(user_id).split()
    if zsite_id in id_list:
        id_list.remove(zsite_id)

    SiteRecNew.set(user_id, ' '.join(map(str,id_list)))

    top_rec_unmark(user_id, TOP_REC_CID_SITE_REC)

def site_rec_set(user_id, site_id):
    SiteRecNew.set(user_id, ' '.join([str(i) for i in site_id]))
    top_rec_mark(user_id, TOP_REC_CID_SITE_REC)

if __name__ == '__main__':
    from model.zsite_url import id_by_url
    jid = id_by_url('jandan')
    from zweb.orm import ormiter
    for i in ormiter(SiteRecHistory):
        print i.id
