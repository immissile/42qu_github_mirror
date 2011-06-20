#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model._db
from zweb._handler import Base
from model.api_client import api_sign_verify, api_login_verify
from model.api_error import API_ERROR_SIGN, API_ERROR_LOGIN

class ApiBase(Base):
    pass



class ApiSignBase(ApiBase):
    def prepare(self):
        arguments = self.request.arguments
        arguments = dict([
            (k, v[0]) for k, v in arguments.iteritems()
        ])
        if api_sign_verify(arguments):
            super(ApiBase, self).prepare()
        else:
            self.finish(API_ERROR_SIGN)



class ApiLoginBase(ApiSignBase):
    def prepare(self):
        super(ApiBase, self).prepare()
        if self._finished:
            return
        S = self.get_argument("S")
        client_id = self.get_argument('client_id')
        if not api_login_verify(client_id, S):
            self.finish(API_ERROR_LOGIN)


