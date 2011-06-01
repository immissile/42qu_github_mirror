#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.mq import mq_server
from model.feed import mq_mc_flush_zsite_follow
from model.mail import mq_rendermail

def run():
    mq_server()

if __name__ == '__main__':
    run()
