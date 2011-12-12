#coding:utf-8
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase

@urlmap("/j/auth/guide/1")
class AuthGuide1(JLoginBase):
    def post(self):
        result = {}
        self.finish(result)
 
@urlmap("/j/auth/guide/2")
class AuthGuide2(JLoginBase):
    def post(self):
        result = {}
        self.finish(result)


@urlmap("/j/auth/guide/3")
class AuthGuide3(JLoginBase):
    def post(self):
        result = {}
        self.finish(result)

