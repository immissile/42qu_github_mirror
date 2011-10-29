#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.follow import Follow
from zweb.orm import ormiter
from model.site_rec import SiteRecHistory

@single_process
def main():

    for i in ormiter(Follow):
        print i.from_id, i.to_id

    for i in ormiter(SiteRecHistory):
        print i.zsite_id, i.user_id, i.state

if __name__ == '__main__':
    main()
