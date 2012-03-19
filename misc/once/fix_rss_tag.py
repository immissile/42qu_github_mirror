#coding:utf-8
import _env
from model.zsite import Zsite
from model.cid import CID_USER , CID_TAG
from model.rss import RssPoId,RssPo
from zweb.orm import ormiter
from model.po import Po

for i in ormiter(RssPoId, "user_cid=%s"%CID_USER):
    po = Po.mc_get(i.po_id)
    rss_po = RssPo.get(i.rss_po_id)
    if po and rss_po:
        po.rid = rss_po.rss_id
        po.save()
        print po.id, rss_id.rss_id

o = Zsite.get(name='kvm')
if o:
    o.name = ''
    o.save()

for i in Zsite.where(cid=CID_TAG):
    if "/" not in i.name:
        from model.po_tag import _tag_alias_new
        _tag_alias_new(i.id, i.name) 



if __name__ == "__main__":
    pass



