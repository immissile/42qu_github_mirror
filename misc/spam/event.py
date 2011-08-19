#coding:utf-8
import _env
from mail import rendermail

mail = "zsp007@gmail.com"
name = "张沈鹏"

rendermail(
    '/mail/spam/event_20110819.htm', mail, name,
    format='html',
    subject='道可道 . 线下活动: 42区 . 技术 . 创业 . 第一讲'
)
