#coding:utf-8
import _env
from model.mail import rendermail
from model.mail_notice import mail_notice_iter, CID_MAIL_MONTH
import time
import traceback


if __name__ == '__main__':
    goon = False
    for mail, name in mail_notice_iter(CID_MAIL_MONTH):
        if mail == 'yupbank@42qu.com':
            goon = True

        if not goon:
            continue
        # print mail


        try:
            rendermail(
                '/mail/spam/event_20110819.htm', mail, name,
                format='html',
                subject='42区 : 技术 . 创业 . 第一讲 - 线下活动 报名 ( 2011年08月21日 星期日 )'
            )
        except:
            traceback.print_exc()
            continue

        print mail

        time.sleep(0.1)
