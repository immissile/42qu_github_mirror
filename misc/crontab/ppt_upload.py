#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env

from model.ppt import Ppt
from zkit.single_process import single_process
from time import time

@single_process
def main():
    now = time() - 200
    for p in Ppt.where(state=1).where('time<%s'%now):
        p.publish()

    for p in Ppt.where(state=0):
        p.upload()



if __name__ == '__main__':
    main()


