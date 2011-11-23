#coding:utf-8


SITE_REC_STATE_REJECT = 0
SITE_REC_STATE_PASS = 1
SITE_REC_STATE_FAV = 2
SITE_REC_STATE = (0,1,2)



from _db import cursor_by_table, McModel,  McCache, McNum, Model, McCacheM, McCacheA
from model.zsite import Zsite
from kv import Kv
from model.zsite import  Zsite
from model.cid import CID_SITE
from model.zsite_fav import zsite_fav_new
from model.top_rec import top_rec_unmark, TOP_REC_CID_SITE_REC, top_rec_mark


SiteRec = Kv('site_rec', 0)

class SiteRecHistory(Model):
    pass

def site_rec(user_id):
    zsite_id = SiteRec.get(user_id)
    if zsite_id:
        return Zsite.mc_get(zsite_id)



def site_rec_feeckback(user_id, zsite_id, state):
    site = Zsite.mc_get(zsite_id)
    state = int(state)

    if not (site and site.cid == CID_SITE):
        return

    if state not in SITE_REC_STATE:
        return


    if state == SITE_REC_STATE_FAV:
        zsite_fav_new(site, user_id)

    SiteRecHistory(
        user_id=user_id, zsite_id=zsite_id, state=state
    ).save()

    SiteRec.set(user_id, 0)
    top_rec_unmark(user_id, TOP_REC_CID_SITE_REC)

def site_rec_set(user_id, site_id):
    SiteRec.set(user_id, site_id)
    top_rec_mark(user_id, TOP_REC_CID_SITE_REC)

if __name__ == "__main__":
    from model.zsite_url import id_by_url
    jid = id_by_url("jandan")
    from zweb.orm import ormiter
    for i in ormiter(SiteRecHistory):
        print i.id
