#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model._db
from zweb._handler import Base
from model.api_key import api_sign_verify
from model.api_error import API_ERROR_SIGN

class ApiBase(Base):
    pass

class ApiSignBase(ApiBase):
    def prepare(self):
        arguments = self.request.arguments
        if api_sign_verify(arguments):
            self.finish(API_ERROR_SIGN)
        else:
            super(ApiBase, self).prepare()


