#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model._db
from zweb._handler import Base
from model.api_client import api_sign_verify
from model.api_error import API_ERROR_SIGN

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


