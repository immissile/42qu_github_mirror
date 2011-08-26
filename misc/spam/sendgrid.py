#coding:utf-8
import json
import re
import textwrap

class SmtpApiHeader:
    def __init__(self):
        self.data = {}

    def addTo(self, to):
        if not self.date.has_key('to'):
            self.data['to'] = []
        if type(to) is str:
            self.data['to'] += [to]
        else:
            self.data['to'] += to

    def addSubVal
