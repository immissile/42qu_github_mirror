#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.oauth import OauthToken
from model.oauth_verify import oauth_verify_by_oauth_id
from zweb.orm import ormiter


@single_process
def oauth_verify():
    for i in ormiter(OauthToken):
        oauth_verify_by_oauth_id(i.id)



if __name__ == '__main__':
    oauth_verify()
