#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from config import PRIVILEGE_ADMIN, PRIVILEGE_SUPER 
from config.privilege import PRIVILEGE_IMPORT_FEED

PRIVILEGE_DICT = {
    PRIVILEGE_IMPORT_FEED:'/import_feed',
}

PRIVILEGE_CN = {
    PRIVILEGE_IMPORT_FEED:"热文推荐审核"
}

PRIVILEGE_ADMIN_DICT = dict(PRIVILEGE_ADMIN)

def page_is_allowed_by_user_id_path(user_id, path):

    if user_id in  PRIVILEGE_SUPER:
        return True

    if path == "/" or path.startswith("/chart"):
        return True

    cid_list = PRIVILEGE_ADMIN_DICT.get(user_id,[])

    for cid in cid_list:
        prefix = PRIVILEGE_DICT[cid]
        if prefix.startswith(prefix):
            return True




if __name__ == '__main__':
    #part_time_job_new(1, 1, 10001517)
    pass
