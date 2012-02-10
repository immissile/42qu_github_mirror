#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from time import time
from config import PRIVILEGE_ADMIN, PRIVILEGE_SUPER 
from config.privilege import PRIVILEGE_FEED_IMPORT

PRIVILEGE_DICT = {
    PRIVILEGE_FEED_IMPORT:'/feed_import',
}

PRIVILEGE_CN = {
    PRIVILEGE_FEED_IMPORT:"热文推荐"
}

PRIVILEGE_ADMIN_DICT = dict(PRIVILEGE_ADMIN)

def has_privilege_by_user_id_path(user_id, path):

    if user_id in  PRIVILEGE_SUPER:
        return True

    if path == "/" or path.startswith("/chart"):
        return True

    cid_list = PRIVILEGE_ADMIN_DICT.get(user_id,[])
    
    for cid in cid_list:
        prefix = PRIVILEGE_DICT[cid]

        if path.startswith(prefix):
            return True

    return False


if __name__ == '__main__':
    print has_privilege_by_user_id_path(10014590,"/z")
