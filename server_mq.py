#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.mq import mq_server
from model.feed import mq_feed_rt_rm_by_rid
from model.mail import mq_rendermail
from model.buzz import mq_buzz_follow_new, mq_buzz_wall_new, mq_buzz_po_reply_new, mq_buzz_po_reply_rm, mq_buzz_po_rm
from model.notice import mq_notice_event_notice, mq_notice_question, mq_invite_question_mail
from model.pic import mq_pic_rm_mail
from model.zsite import mq_zsite_verify_mail
from model.event import mq_event_kill_extra

def run():
    mq_server()

if __name__ == '__main__':
    run()
