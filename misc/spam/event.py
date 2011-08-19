#coding:utf-8
import _env
from model.mail import rendermail

mail = "zsp007@gmail.com"
name = "张沈鹏"
mail = "yupbank@gmail.com"
name = "于鹏"

rendermail(
    '/mail/spam/event_20110819.htm', mail, name,
    format='html',
    subject='42区 线下活动 报名 : 技术 . 创业 . 第一讲'
)
