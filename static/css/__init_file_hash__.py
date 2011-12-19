#coding:utf-8


from config import DEBUG
from config import FS_URL

if DEBUG:
    ORG_CSS_JS = True
else:
    ORG_CSS_JS = False


if ORG_CSS_JS:

    ctrl_com_bio_ = "%s/css/ctrl/com/bio.css"%FS_URL
    ctrl_com_bio = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_com_bio_

    ctrl_fav_ = "%s/css/ctrl/fav.css"%FS_URL
    ctrl_fav = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_fav_

    ctrl_site_admin_ = "%s/css/ctrl/site/admin.css"%FS_URL
    ctrl_site_admin = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_site_admin_

    ctrl_layout_ = "%s/css/ctrl/layout.css"%FS_URL
    ctrl_layout = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_layout_

    ctrl_zsite_com_guide_ = "%s/css/ctrl/zsite/com/guide.css"%FS_URL
    ctrl_zsite_com_guide = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_zsite_com_guide_

    ctrl_zsite_com_list_ = "%s/css/ctrl/zsite/com_list.css"%FS_URL
    ctrl_zsite_com_list = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_zsite_com_list_

    ctrl_index_ = "%s/css/ctrl/index.css"%FS_URL
    ctrl_index = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_index_

    ctrl_hero_ = "%s/css/ctrl/hero.css"%FS_URL
    ctrl_hero = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_hero_

    ctrl_i_ = "%s/css/ctrl/i.css"%FS_URL
    ctrl_i = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_i_

    ctrl_live_ = "%s/css/ctrl/live.css"%FS_URL
    ctrl_live = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_live_

    ctrl_follow_zsite_ = "%s/css/ctrl/follow/zsite.css"%FS_URL
    ctrl_follow_zsite = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_follow_zsite_

    zpage_ = "%s/css/zpage.css"%FS_URL
    zpage = '<link href="%s" rel="stylesheet" type="text/css">' % zpage_

    ctrl_po_event_add_ = "%s/css/ctrl/po/event_add.css"%FS_URL
    ctrl_po_event_add = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_po_event_add_

    imgselect_ = "%s/css/imgselect.css"%FS_URL
    imgselect = '<link href="%s" rel="stylesheet" type="text/css">' % imgselect_

    synhigh_shThemeRDark_ = "%s/css/synhigh/shThemeRDark.css"%FS_URL
    synhigh_shThemeRDark = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shThemeRDark_

    ctrl_main_ = "%s/css/ctrl/main.css"%FS_URL
    ctrl_main = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_main_

    ctrl_site_index_ = "%s/css/ctrl/site/index.css"%FS_URL
    ctrl_site_index = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_site_index_

    ctrl_i_password_ = "%s/css/ctrl/i/password.css"%FS_URL
    ctrl_i_password = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_i_password_

    ctrl_qtip_ = "%s/css/ctrl/qtip.css"%FS_URL
    ctrl_qtip = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_qtip_

    ctrl_po_edit_ = "%s/css/ctrl/po/edit.css"%FS_URL
    ctrl_po_edit = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_po_edit_

    ctrl_feed_ = "%s/css/ctrl/feed.css"%FS_URL
    ctrl_feed = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_feed_

    ctrl_site_rec_ = "%s/css/ctrl/site/rec.css"%FS_URL
    ctrl_site_rec = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_site_rec_

    istarsea_ = "%s/css/istarsea.css"%FS_URL
    istarsea = '<link href="%s" rel="stylesheet" type="text/css">' % istarsea_

    synhigh_shCoreMidnight_ = "%s/css/synhigh/shCoreMidnight.css"%FS_URL
    synhigh_shCoreMidnight = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shCoreMidnight_

    god_zsite_book_ = "%s/css/god/zsite_book.css"%FS_URL
    god_zsite_book = '<link href="%s" rel="stylesheet" type="text/css">' % god_zsite_book_

    synhigh_shCoreEclipse_ = "%s/css/synhigh/shCoreEclipse.css"%FS_URL
    synhigh_shCoreEclipse = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shCoreEclipse_

    ctrl_event_joiner_ = "%s/css/ctrl/event/joiner.css"%FS_URL
    ctrl_event_joiner = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_event_joiner_

    ctrl_event_join_ = "%s/css/ctrl/event/join.css"%FS_URL
    ctrl_event_join = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_event_join_

    synhigh_shCoreEmacs_ = "%s/css/synhigh/shCoreEmacs.css"%FS_URL
    synhigh_shCoreEmacs = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shCoreEmacs_

    ctrl_po_tag_ = "%s/css/ctrl/po/tag.css"%FS_URL
    ctrl_po_tag = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_po_tag_

    ctrl_site_admin_admin_review_ = "%s/css/ctrl/site/admin/admin_review.css"%FS_URL
    ctrl_site_admin_admin_review = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_site_admin_admin_review_

    synhigh_shThemeDefault_ = "%s/css/synhigh/shThemeDefault.css"%FS_URL
    synhigh_shThemeDefault = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shThemeDefault_

    synhigh_shCore_ = "%s/css/synhigh/shCore.css"%FS_URL
    synhigh_shCore = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shCore_

    synhigh_shCoreDefault_ = "%s/css/synhigh/shCoreDefault.css"%FS_URL
    synhigh_shCoreDefault = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shCoreDefault_

    ctrl_i_invite_ = "%s/css/ctrl/i/invite.css"%FS_URL
    ctrl_i_invite = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_i_invite_

    ctrl_me_newbie_ = "%s/css/ctrl/me/newbie.css"%FS_URL
    ctrl_me_newbie = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_me_newbie_

    ctrl_com_index_ = "%s/css/ctrl/com/index.css"%FS_URL
    ctrl_com_index = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_com_index_

    ctrl_zsite_com_job_ = "%s/css/ctrl/zsite/com/job.css"%FS_URL
    ctrl_zsite_com_job = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_zsite_com_job_

    ctrl_auth_reg_ = "%s/css/ctrl/auth/reg.css"%FS_URL
    ctrl_auth_reg = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_auth_reg_

    ctrl_po_event_ = "%s/css/ctrl/po/event.css"%FS_URL
    ctrl_po_event = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_po_event_

    ctrl_event_admin_ = "%s/css/ctrl/event/admin.css"%FS_URL
    ctrl_event_admin = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_event_admin_

    synhigh_shCoreRDark_ = "%s/css/synhigh/shCoreRDark.css"%FS_URL
    synhigh_shCoreRDark = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shCoreRDark_

    reset_ = "%s/css/reset.css"%FS_URL
    reset = '<link href="%s" rel="stylesheet" type="text/css">' % reset_

    base_ = "%s/css/base.css"%FS_URL
    base = '<link href="%s" rel="stylesheet" type="text/css">' % base_

    synhigh_shCoreMDUltra_ = "%s/css/synhigh/shCoreMDUltra.css"%FS_URL
    synhigh_shCoreMDUltra = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shCoreMDUltra_

    synhigh_shCoreDjango_ = "%s/css/synhigh/shCoreDjango.css"%FS_URL
    synhigh_shCoreDjango = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shCoreDjango_

    god_review_ = "%s/css/god/review.css"%FS_URL
    god_review = '<link href="%s" rel="stylesheet" type="text/css">' % god_review_

    ctrl_com_job_ = "%s/css/ctrl/com/job.css"%FS_URL
    ctrl_com_job = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_com_job_

    ctrl_school_ = "%s/css/ctrl/school.css"%FS_URL
    ctrl_school = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_school_

    ctrl_po_ = "%s/css/ctrl/po.css"%FS_URL
    ctrl_po = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_po_

    ctrl_product_ = "%s/css/ctrl/product.css"%FS_URL
    ctrl_product = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_product_

    ctrl_i_namecard_ = "%s/css/ctrl/i/namecard.css"%FS_URL
    ctrl_i_namecard = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_i_namecard_

    ctrl_zsite_com_ = "%s/css/ctrl/zsite/com.css"%FS_URL
    ctrl_zsite_com = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_zsite_com_

    ctrl_com_member_ = "%s/css/ctrl/com/member.css"%FS_URL
    ctrl_com_member = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_com_member_

    ctrl_box_login_ = "%s/css/ctrl/box/login.css"%FS_URL
    ctrl_box_login = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_box_login_

    god_chart_ = "%s/css/god/chart.css"%FS_URL
    god_chart = '<link href="%s" rel="stylesheet" type="text/css">' % god_chart_

    ctrl_po_event_page_ = "%s/css/ctrl/po/event_page.css"%FS_URL
    ctrl_po_event_page = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_po_event_page_

    meet_ = "%s/css/meet.css"%FS_URL
    meet = '<link href="%s" rel="stylesheet" type="text/css">' % meet_

    synhigh_shThemeMDUltra_ = "%s/css/synhigh/shThemeMDUltra.css"%FS_URL
    synhigh_shThemeMDUltra = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shThemeMDUltra_

    ctrl_zsite_site_ = "%s/css/ctrl/zsite/site.css"%FS_URL
    ctrl_zsite_site = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_zsite_site_

    ctrl_site_new_ = "%s/css/ctrl/site/new.css"%FS_URL
    ctrl_site_new = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_site_new_

    synhigh_shThemeEmacs_ = "%s/css/synhigh/shThemeEmacs.css"%FS_URL
    synhigh_shThemeEmacs = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shThemeEmacs_

    ctrl_zsite_ = "%s/css/ctrl/zsite.css"%FS_URL
    ctrl_zsite = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_zsite_

    ctrl_main_share_ = "%s/css/ctrl/main/share.css"%FS_URL
    ctrl_main_share = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_main_share_

    jquery_fancybox_1_3_4_ = "%s/css/jquery.fancybox-1.3.4.css"%FS_URL
    jquery_fancybox_1_3_4 = '<link href="%s" rel="stylesheet" type="text/css">' % jquery_fancybox_1_3_4_

    synhigh_shCoreFadeToGrey_ = "%s/css/synhigh/shCoreFadeToGrey.css"%FS_URL
    synhigh_shCoreFadeToGrey = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shCoreFadeToGrey_

    synhigh_shThemeDjango_ = "%s/css/synhigh/shThemeDjango.css"%FS_URL
    synhigh_shThemeDjango = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shThemeDjango_

    ctrl_com_resume_ = "%s/css/ctrl/com/resume.css"%FS_URL
    ctrl_com_resume = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_com_resume_

    synhigh_shThemeEclipse_ = "%s/css/synhigh/shThemeEclipse.css"%FS_URL
    synhigh_shThemeEclipse = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shThemeEclipse_

    api_0_ = "%s/css/api/0.css"%FS_URL
    api_0 = '<link href="%s" rel="stylesheet" type="text/css">' % api_0_

    ctrl_wall_page_ = "%s/css/ctrl/wall/page.css"%FS_URL
    ctrl_wall_page = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_wall_page_

    synhigh_shThemeFadeToGrey_ = "%s/css/synhigh/shThemeFadeToGrey.css"%FS_URL
    synhigh_shThemeFadeToGrey = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shThemeFadeToGrey_

    ctrl_com_review_ = "%s/css/ctrl/com/review.css"%FS_URL
    ctrl_com_review = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_com_review_

    ctrl_pay_ = "%s/css/ctrl/pay.css"%FS_URL
    ctrl_pay = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_pay_

    ctrl_tag_ = "%s/css/ctrl/tag.css"%FS_URL
    ctrl_tag = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_tag_

    ctrl_me_guide_ = "%s/css/ctrl/me/guide.css"%FS_URL
    ctrl_me_guide = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_me_guide_

    z_ = "%s/css/z.css"%FS_URL
    z = '<link href="%s" rel="stylesheet" type="text/css">' % z_

    god_god_ = "%s/css/god/god.css"%FS_URL
    god_god = '<link href="%s" rel="stylesheet" type="text/css">' % god_god_

    ctrl_i_career_ = "%s/css/ctrl/i/career.css"%FS_URL
    ctrl_i_career = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_i_career_

    ctrl_i_link_ = "%s/css/ctrl/i/link.css"%FS_URL
    ctrl_i_link = '<link href="%s" rel="stylesheet" type="text/css">' % ctrl_i_link_

    synhigh_shThemeMidnight_ = "%s/css/synhigh/shThemeMidnight.css"%FS_URL
    synhigh_shThemeMidnight = '<link href="%s" rel="stylesheet" type="text/css">' % synhigh_shThemeMidnight_

else:

    ctrl_com_bio_ = "%s/css/ctrl/com/~rPiAQ~bio.css"%FS_URL
    ctrl_com_bio = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_com_bio_

    ctrl_fav_ = "%s/css/ctrl/~rPiAQ~fav.css"%FS_URL
    ctrl_fav = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_fav_

    ctrl_site_admin_ = "%s/css/ctrl/site/~rPiAQ~admin.css"%FS_URL
    ctrl_site_admin = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_site_admin_

    ctrl_layout_ = "%s/css/ctrl/~rPiAQ~layout.css"%FS_URL
    ctrl_layout = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_layout_

    ctrl_zsite_com_guide_ = "%s/css/ctrl/zsite/com/~rPiAQ~guide.css"%FS_URL
    ctrl_zsite_com_guide = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_zsite_com_guide_

    ctrl_zsite_com_list_ = "%s/css/ctrl/zsite/~rPiAQ~com_list.css"%FS_URL
    ctrl_zsite_com_list = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_zsite_com_list_

    ctrl_index_ = "%s/css/ctrl/~rPiCA~index.css"%FS_URL
    ctrl_index = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_index_

    ctrl_hero_ = "%s/css/ctrl/~rPiAQ~hero.css"%FS_URL
    ctrl_hero = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_hero_

    ctrl_i_ = "%s/css/ctrl/~rPiAQ~i.css"%FS_URL
    ctrl_i = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_i_

    ctrl_live_ = "%s/css/ctrl/~rPiAQ~live.css"%FS_URL
    ctrl_live = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_live_

    ctrl_follow_zsite_ = "%s/css/ctrl/follow/~rPiAQ~zsite.css"%FS_URL
    ctrl_follow_zsite = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_follow_zsite_

    zpage_ = "%s/css/~rPiAQ~zpage.css"%FS_URL
    zpage = '<link href="%s" rel="stylesheet" type="text/css">'%zpage_

    ctrl_po_event_add_ = "%s/css/ctrl/po/~rPiAQ~event_add.css"%FS_URL
    ctrl_po_event_add = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_po_event_add_

    imgselect_ = "%s/css/~rPiAQ~imgselect.css"%FS_URL
    imgselect = '<link href="%s" rel="stylesheet" type="text/css">'%imgselect_

    synhigh_shThemeRDark_ = "%s/css/synhigh/~rPiAQ~shThemeRDark.css"%FS_URL
    synhigh_shThemeRDark = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shThemeRDark_

    ctrl_main_ = "%s/css/ctrl/~rPiAg~main.css"%FS_URL
    ctrl_main = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_main_

    ctrl_site_index_ = "%s/css/ctrl/site/~rPiAQ~index.css"%FS_URL
    ctrl_site_index = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_site_index_

    ctrl_i_password_ = "%s/css/ctrl/i/~rPiAQ~password.css"%FS_URL
    ctrl_i_password = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_i_password_

    ctrl_qtip_ = "%s/css/ctrl/~rPiAQ~qtip.css"%FS_URL
    ctrl_qtip = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_qtip_

    ctrl_po_edit_ = "%s/css/ctrl/po/~rPiAQ~edit.css"%FS_URL
    ctrl_po_edit = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_po_edit_

    ctrl_feed_ = "%s/css/ctrl/~rPiAQ~feed.css"%FS_URL
    ctrl_feed = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_feed_

    ctrl_site_rec_ = "%s/css/ctrl/site/~rPiAQ~rec.css"%FS_URL
    ctrl_site_rec = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_site_rec_

    istarsea_ = "%s/css/~rPiBg~istarsea.css"%FS_URL
    istarsea = '<link href="%s" rel="stylesheet" type="text/css">'%istarsea_

    synhigh_shCoreMidnight_ = "%s/css/synhigh/~rPiAQ~shCoreMidnight.css"%FS_URL
    synhigh_shCoreMidnight = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shCoreMidnight_

    god_zsite_book_ = "%s/css/god/~rPiAQ~zsite_book.css"%FS_URL
    god_zsite_book = '<link href="%s" rel="stylesheet" type="text/css">'%god_zsite_book_

    synhigh_shCoreEclipse_ = "%s/css/synhigh/~rPiAQ~shCoreEclipse.css"%FS_URL
    synhigh_shCoreEclipse = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shCoreEclipse_

    ctrl_event_joiner_ = "%s/css/ctrl/event/~rPiAQ~joiner.css"%FS_URL
    ctrl_event_joiner = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_event_joiner_

    ctrl_event_join_ = "%s/css/ctrl/event/~rPiAQ~join.css"%FS_URL
    ctrl_event_join = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_event_join_

    synhigh_shCoreEmacs_ = "%s/css/synhigh/~rPiAQ~shCoreEmacs.css"%FS_URL
    synhigh_shCoreEmacs = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shCoreEmacs_

    ctrl_po_tag_ = "%s/css/ctrl/po/~rPiAQ~tag.css"%FS_URL
    ctrl_po_tag = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_po_tag_

    ctrl_site_admin_admin_review_ = "%s/css/ctrl/site/admin/~rPiAQ~admin_review.css"%FS_URL
    ctrl_site_admin_admin_review = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_site_admin_admin_review_

    synhigh_shThemeDefault_ = "%s/css/synhigh/~rPiAQ~shThemeDefault.css"%FS_URL
    synhigh_shThemeDefault = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shThemeDefault_

    synhigh_shCore_ = "%s/css/synhigh/~rPiAQ~shCore.css"%FS_URL
    synhigh_shCore = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shCore_

    synhigh_shCoreDefault_ = "%s/css/synhigh/~rPiAQ~shCoreDefault.css"%FS_URL
    synhigh_shCoreDefault = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shCoreDefault_

    ctrl_i_invite_ = "%s/css/ctrl/i/~rPiAQ~invite.css"%FS_URL
    ctrl_i_invite = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_i_invite_

    ctrl_me_newbie_ = "%s/css/ctrl/me/~rPiAQ~newbie.css"%FS_URL
    ctrl_me_newbie = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_me_newbie_

    ctrl_com_index_ = "%s/css/ctrl/com/~rPiAQ~index.css"%FS_URL
    ctrl_com_index = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_com_index_

    ctrl_zsite_com_job_ = "%s/css/ctrl/zsite/com/~rPiAQ~job.css"%FS_URL
    ctrl_zsite_com_job = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_zsite_com_job_

    ctrl_auth_reg_ = "%s/css/ctrl/auth/~rPiAQ~reg.css"%FS_URL
    ctrl_auth_reg = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_auth_reg_

    ctrl_po_event_ = "%s/css/ctrl/po/~rPiAQ~event.css"%FS_URL
    ctrl_po_event = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_po_event_

    ctrl_event_admin_ = "%s/css/ctrl/event/~rPiAQ~admin.css"%FS_URL
    ctrl_event_admin = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_event_admin_

    synhigh_shCoreRDark_ = "%s/css/synhigh/~rPiAQ~shCoreRDark.css"%FS_URL
    synhigh_shCoreRDark = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shCoreRDark_

    reset_ = "%s/css/~rPiAg~reset.css"%FS_URL
    reset = '<link href="%s" rel="stylesheet" type="text/css">'%reset_

    base_ = "%s/css/~rPiAQ~base.css"%FS_URL
    base = '<link href="%s" rel="stylesheet" type="text/css">'%base_

    synhigh_shCoreMDUltra_ = "%s/css/synhigh/~rPiAQ~shCoreMDUltra.css"%FS_URL
    synhigh_shCoreMDUltra = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shCoreMDUltra_

    synhigh_shCoreDjango_ = "%s/css/synhigh/~rPiAQ~shCoreDjango.css"%FS_URL
    synhigh_shCoreDjango = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shCoreDjango_

    god_review_ = "%s/css/god/~rPiAQ~review.css"%FS_URL
    god_review = '<link href="%s" rel="stylesheet" type="text/css">'%god_review_

    ctrl_com_job_ = "%s/css/ctrl/com/~rPiAQ~job.css"%FS_URL
    ctrl_com_job = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_com_job_

    ctrl_school_ = "%s/css/ctrl/~rPiAQ~school.css"%FS_URL
    ctrl_school = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_school_

    ctrl_po_ = "%s/css/ctrl/~rPiAg~po.css"%FS_URL
    ctrl_po = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_po_

    ctrl_product_ = "%s/css/ctrl/~rPiAQ~product.css"%FS_URL
    ctrl_product = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_product_

    ctrl_i_namecard_ = "%s/css/ctrl/i/~rPiAQ~namecard.css"%FS_URL
    ctrl_i_namecard = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_i_namecard_

    ctrl_zsite_com_ = "%s/css/ctrl/zsite/~rPiAg~com.css"%FS_URL
    ctrl_zsite_com = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_zsite_com_

    ctrl_com_member_ = "%s/css/ctrl/com/~rPiAQ~member.css"%FS_URL
    ctrl_com_member = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_com_member_

    ctrl_box_login_ = "%s/css/ctrl/box/~rPiAQ~login.css"%FS_URL
    ctrl_box_login = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_box_login_

    god_chart_ = "%s/css/god/~rPiAQ~chart.css"%FS_URL
    god_chart = '<link href="%s" rel="stylesheet" type="text/css">'%god_chart_

    ctrl_po_event_page_ = "%s/css/ctrl/po/~rPiAQ~event_page.css"%FS_URL
    ctrl_po_event_page = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_po_event_page_

    meet_ = "%s/css/~rPiAQ~meet.css"%FS_URL
    meet = '<link href="%s" rel="stylesheet" type="text/css">'%meet_

    synhigh_shThemeMDUltra_ = "%s/css/synhigh/~rPiAQ~shThemeMDUltra.css"%FS_URL
    synhigh_shThemeMDUltra = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shThemeMDUltra_

    ctrl_zsite_site_ = "%s/css/ctrl/zsite/~rPiAQ~site.css"%FS_URL
    ctrl_zsite_site = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_zsite_site_

    ctrl_site_new_ = "%s/css/ctrl/site/~rPiAQ~new.css"%FS_URL
    ctrl_site_new = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_site_new_

    synhigh_shThemeEmacs_ = "%s/css/synhigh/~rPiAQ~shThemeEmacs.css"%FS_URL
    synhigh_shThemeEmacs = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shThemeEmacs_

    ctrl_zsite_ = "%s/css/ctrl/~rPiAQ~zsite.css"%FS_URL
    ctrl_zsite = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_zsite_

    ctrl_main_share_ = "%s/css/ctrl/main/~rPiAQ~share.css"%FS_URL
    ctrl_main_share = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_main_share_

    jquery_fancybox_1_3_4_ = "%s/css/~rPiAQ~jquery.fancybox-1.3.4.css"%FS_URL
    jquery_fancybox_1_3_4 = '<link href="%s" rel="stylesheet" type="text/css">'%jquery_fancybox_1_3_4_

    synhigh_shCoreFadeToGrey_ = "%s/css/synhigh/~rPiAQ~shCoreFadeToGrey.css"%FS_URL
    synhigh_shCoreFadeToGrey = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shCoreFadeToGrey_

    synhigh_shThemeDjango_ = "%s/css/synhigh/~rPiAQ~shThemeDjango.css"%FS_URL
    synhigh_shThemeDjango = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shThemeDjango_

    ctrl_com_resume_ = "%s/css/ctrl/com/~rPiAQ~resume.css"%FS_URL
    ctrl_com_resume = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_com_resume_

    synhigh_shThemeEclipse_ = "%s/css/synhigh/~rPiAQ~shThemeEclipse.css"%FS_URL
    synhigh_shThemeEclipse = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shThemeEclipse_

    api_0_ = "%s/css/api/~rPiAQ~0.css"%FS_URL
    api_0 = '<link href="%s" rel="stylesheet" type="text/css">'%api_0_

    ctrl_wall_page_ = "%s/css/ctrl/wall/~rPiAQ~page.css"%FS_URL
    ctrl_wall_page = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_wall_page_

    synhigh_shThemeFadeToGrey_ = "%s/css/synhigh/~rPiAQ~shThemeFadeToGrey.css"%FS_URL
    synhigh_shThemeFadeToGrey = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shThemeFadeToGrey_

    ctrl_com_review_ = "%s/css/ctrl/com/~rPiAQ~review.css"%FS_URL
    ctrl_com_review = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_com_review_

    ctrl_pay_ = "%s/css/ctrl/~rPiAQ~pay.css"%FS_URL
    ctrl_pay = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_pay_

    ctrl_tag_ = "%s/css/ctrl/~rPiAQ~tag.css"%FS_URL
    ctrl_tag = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_tag_

    ctrl_me_guide_ = "%s/css/ctrl/me/~rPiAQ~guide.css"%FS_URL
    ctrl_me_guide = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_me_guide_

    z_ = "%s/css/~rPiAQ~z.css"%FS_URL
    z = '<link href="%s" rel="stylesheet" type="text/css">'%z_

    god_god_ = "%s/css/god/~rPiAQ~god.css"%FS_URL
    god_god = '<link href="%s" rel="stylesheet" type="text/css">'%god_god_

    ctrl_i_career_ = "%s/css/ctrl/i/~rPiAQ~career.css"%FS_URL
    ctrl_i_career = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_i_career_

    ctrl_i_link_ = "%s/css/ctrl/i/~rPiAQ~link.css"%FS_URL
    ctrl_i_link = '<link href="%s" rel="stylesheet" type="text/css">'%ctrl_i_link_

    synhigh_shThemeMidnight_ = "%s/css/synhigh/~rPiAQ~shThemeMidnight.css"%FS_URL
    synhigh_shThemeMidnight = '<link href="%s" rel="stylesheet" type="text/css">'%synhigh_shThemeMidnight_
