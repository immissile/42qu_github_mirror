#coding:utf-8
import _env
from model.mail import rendermail
from model.mail_notice import mail_notice_iter, CID_MAIL_MONTH
import time

if __name__ == "__main__":
    for mail, name in mail_notice_iter(CID_MAIL_MONTH):
        #mail = "zsp007@gmail.com"

        rendermail(
            '/mail/spam/event_20110819.htm', mail, name,
            format='html',
            subject='42区 : 技术 . 创业 . 第一讲 - 线下活动 报名 ( 2011年08月21日 星期日 )'
        )
        time.sleep(0.1)
