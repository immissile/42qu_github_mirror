#!/usr/bin/env python
# -*- coding: utf-8 -*-
SPAM_USER_ID = set((
    10009078, #欲望清单 www.desirelist.nst
    10003899, #欲望清单 www.desirelist.nst
    10011921,
    10022520,
))

def is_spammer(user_id):
    if int(user_id) in SPAM_USER_ID:
        return True

if __name__ == '__main__':
    print is_spammer(14)
