#coding:utf-8
import _env
from model.feed_import import PoMetaUser, FeedImport
from model.zsite import zsite_by_query , Zsite
from model.user_mail import user_by_mail
from model.ico import pic_url
from model.feed_import_user import feed_import_user_new

count = 0
with open('ucd.csv') as ucd:
    for line in ucd:
        line = line.decode('gb18030')
        t = line.split(',')
        if len(t) != 6:
            print line
        else:
            uid = t[0].split(' ', 1)[0]
            u = PoMetaUser.mc_get(uid)
            link = t[4]

            zsite = None

            if link:
                id = zsite_by_query(link)
                zsite = Zsite.mc_get(id)
            else:
                email = t[5].strip()
                if email:
                    zsite = user_by_mail(email)


            if zsite:
                user_id = zsite.id
                if pic_url(user_id):
                    for i in FeedImport.where(po_meta_user_id=u.id):
                        feed_import_user_new(user_id, i.id)

                    #    print i.title
                    #print zsite.name, "http:"+zsite.link
                    #print u.name , u.link
                    #count += 1
                    #print count , zsite.id
                    #print ''
                    #u.user_id = zsite.id
                    #u.save()


