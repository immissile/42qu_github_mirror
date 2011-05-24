#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import cursor_by_table, McModel, McLimitA, McCache

class PoPic(McModel):
    pass


PIC_LIMIT = 42

#PIC_SAFE = 30
#PIC_ADD = 20
#PIC_SELF_DELETE = 10
#PIC_UNSAFE = 5
#PIC_ANTI = 0

PIC_SIZE = 684
PIC_THUMB_SIZE = 219
#PIC_LIST_SIZE = (219, 123)
#PIC_LIST_PATH = '%s_%s' % PIC_LIST_SIZE

PIC_LEFT = 1
PIC_CENTER = 0
PIC_RIGHT = 2


def pic_id_list(self):
    return PoPic.where(rid=self.id).order_by('seq desc').id_list()


def pic_new_id_list(cls, user_id):
    return PoPic.where(rid=0, user_id=user_id).order_by('seq desc').id_list()


PIC_FIND = re.compile(r'<图片([\d]+)>')
PIC_SUB = re.compile(r'&lt;图片([\d]+)&gt;')
PIC_HTML = '<div class="pmix np%s"><img src="%s" alt="%s"><div>%s</div></div>'

def pic2html(match, d):
    m = int(match.groups()[0])
    return d.get(m, match.group(0))


def html_by_rid(self):
    return txt_to_pic_html(self.txt, self.pic_show_dic)


def txt_to_pic_html(txt, pic_dic):
    return PIC_SUB.sub(lambda x: pic2html(x, pic_dic), txt_withlink(txt))


class PicMixin(object):

    @classmethod
    def can_new_pic(cls, user_id, rid=0):
        c = PoPic.where(user_id=user_id, rid=rid).count()
        return c < PIC_LIMIT

    @classmethod
    def get_pic_order(cls, user_id, rid=0):
        c = PoPic.raw_sql('select max(seq) from po_pic where user_id=%s and rid=%s', user_id, rid)
        seq = c.fetchone()[0] or 0
        return seq + 1

    @classmethod
    def new_pic(cls, user_id, rid, img):
        order = cls.get_pic_order(user_id, rid)
        pic_id = pic_new(user_id)
        pic = PoPic(id=pic_id, user_id=user_id, rid=rid, order=order)
        pic.save()

        cls.store_pic(pic_id, img)
        cls.mc_flush_pic(user_id, rid)
        return pic

    @classmethod
    def store_pic(cls, pic_id, img):
        prefix = cls.Meta.table

        fs_set_jpg('2', pic_id, p1)

        _img = pic_fit_width_cut_height_if_large(img, PIC_SIZE)
        fs_set_jpg('%s/%s' % (prefix, PIC_SIZE), pic_id, _img)

        _img = pic_fit_width_cut_height_if_large(img, PIC_THUMB_SIZE)
        fs_set_jpg('%s/%s' % (prefix, PIC_THUMB_SIZE), pic_id, _img)

#        _img = pic_fit(img, *PIC_LIST_SIZE)
#        fs_set_jpg('%s/%s' % (prefix, PIC_LIST_PATH), pic_id, _img)

    @classmethod
    def rm_pic(cls, user_id, rid, order):
        PoPic.where(user_id=user_id, rid=rid, order=order).where('state>=%s', PIC_ADD).update(state=PIC_SELF_DELETE)
        cls.mc_flush_pic(user_id, rid)

    @classmethod
    def mc_flush_pic(cls, user_id, rid=0):
        if rid:
            cls.mc_pic_id_by_rid.delete(rid)
            cls.mc_html_by_rid.delete(rid)
        else:
            cls.mc_pic_new_by_user_id.delete(user_id)

#    @classmethod
#    def save_pics(cls, pic_list, rid, ):
#        pass

    @property
    def pic_show_dic(self):
        li = PoPic.mc_get_list(self.pic_id_list)
        return dict((i.order, PIC_HTML % (
            i.align,
            fs_url_jpg(i.id, 684),
            escape(i.title).replace('"', '&quot;'),
            escape(i.title)
        )) for i in li)

    @property
    def pic_edit_list(self):
        li = PoPic.mc_get_list(self.pic_id_list)
        for i in li:
            i.src219 = fs_url_jpg(i.id, 219)
        return li

    @classmethod
    def pic_new_list(cls, user_id):
        li = PoPic.mc_get_list(cls.pic_new_id_list(user_id))
        for i in li:
            i.src219 = fs_url_jpg(i.id, 219)
        return li


# CREATE TABLE `xxx_pic` (
#  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#  `rid` int(10) unsigned NOT NULL DEFAULT '0',
#  `user_id` int(10) unsigned NOT NULL,
#  `order` tinyint(3) unsigned NOT NULL,
#  `align` tinyint(3) unsigned NOT NULL DEFAULT '0',
#  `title` varbinary(60) DEFAULT '',
#  PRIMARY KEY (`id`),
#  KEY `rid` (`rid`),
#  KEY `user_id` (`user_id`)
# ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin

def mixin_pic(pic_cls):
    '''
class XxxPic(McModel):
    pass
@mixin_pic(XxxPic)
class Xxx(McModel):
    pass'''
    def _(cls):
        cls.__bases__ = tuple(list(cls.__bases__) + [PicMixin])
        cls._PIC_CLS = pic_cls
        table_title = cls.Meta.table.title()
        cls.mc_pic_id_by_rid = McLimitA(
            'PicIdBy%sId.%%s' % table_title,
            PIC_LIMIT
        )
        cls.mc_pic_new_by_user_id = McCache(
            'PicNewBy%sManId.%%s' % table_title
        )
        cls.mc_html_by_rid = McCache(
            'HtmlBy%sId.%%s' % table_title
        )
        cls.pic_id_list = property(
            cls.mc_pic_id_by_rid('{self.id}')(
            pic_id_list
        ))
        cls.pic_new_id_list = classmethod(
            cls.mc_pic_new_by_user_id('{user_id}')(
            pic_new_id_list
        ))
        cls.html = property(
            cls.mc_html_by_rid('{self.id}')(
            html_by_rid
        ))
        cls._PIC_ORDER_SQL = 'select max(`order`) from %s where user_id=%%s and rid=%%s and state>=%%s' % pic_cls.Meta.table

        return cls
    return _

if __name__ == '__main__':
    pass
