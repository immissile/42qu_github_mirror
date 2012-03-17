#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from model.spammer import spammer_new
from model._db import Model
from zweb.orm import ormiter

class Spammer(Model):
    pass

def main():
    for i in ormiter(Spammer):
        print "spaming",i.id
        spammer_new(i.id)

if __name__ == '__main__':
    main()  
