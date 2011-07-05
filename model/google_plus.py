#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel

class GoogleRank(Model):
    pass


if __name__ == '__main__':
    print urlopen("https://plus.google.com/115113322964276305188").read()

