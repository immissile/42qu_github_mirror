#coding:utf-8
import _env
from model.rss import RssPoId
from model.po import Po
from model.zsite import Zsite

for i in RssPoId.where(rss_po_id=0):
    po = Po.get(i.po_id)
    if not po:
        i.delete()
        continue

    zsite = Zsite.mc_get(po.user_id)
    if not zsite:
        i.delete()
        continue
    print i.id

    i.rss_po_id = i.id
    i.user_id = po.user_id
    i.user_cid = zsite.cid
    i.save() 

#CREATE TABLE  `zpage`.`rss_po_id` (
#  `id` int(10) unsigned NOT NULL,
#  `po_id` int(10) unsigned NOT NULL,
#  `state` int(10) unsigned NOT NULL,
#  `tag_id_list` blob NOT NULL,
#  `rss_po_id` int(10) unsigned NOT NULL default '0',
#  `user_id` int(10) unsigned NOT NULL default '0',
#  `admin_id` int(10) unsigned NOT NULL default '0',
#  `user_cid` int(10) unsigned NOT NULL default '0',
#  PRIMARY KEY  (`id`),
#  KEY `po_id` (`po_id`),
#  KEY `Index_3` (`rss_po_id`)
#) ENGINE=MyISAM DEFAULT CHARSET=binary;        

if __name__ == '__main__':
    pass



