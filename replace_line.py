#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath, dirname, basename, join
from os import walk

FROM_STRING = """

get_feed_2_edit
rm_import_feed
new_import_feed
set_feed_state
get_zsite_user_id
feed_2_po
STATE_ALLOWED_WITHNO_AUTHOR    
STATE_INIT        
STATE_DISALLOWED           
STATE_ALLOWED      
STATE_PO_IS_CREATED
get_most_rec_and_likes
fetch_feed



"""

TO_STRING = """

feed_next
import_feed_rm
import_feed_new
feed_state_set
zsite_id_by_douban_user_id
feed2po
IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR
IMPORT_FEED_STATE_INIT        
IMPORT_FEED_STATE_RM          
IMPORT_FEED_STATE_REVIEWED    
IMPORT_FEED_STATE_POED
douban_feed_to_review_iter
import_feed_by_douban_feed



"""

def run():
    from_string = FROM_STRING.strip()
    to_string = TO_STRING.strip()
    for from_s, to_s in zip(FROM_STRING.split('\n'), TO_STRING.split('\n')):
        replace(from_s.strip(), to_s.strip())

def replace(from_string, to_string):
    from_string = from_string.strip()
    to_string = to_string.strip()

    file = abspath(__file__)

    for dirpath, dirnames, filenames in walk(dirname(file)):
        dirbase = basename(dirpath)
        if dirbase.startswith('.'):
            continue

        for filename in filenames:
            suffix = filename.rsplit('.', 1)[-1]
            if suffix not in ('py', 'htm', 'txt', 'conf', 'css', 'h', 'template', 'js'):
                continue
            path = join(dirpath, filename)
            if path == file:
                continue
            with open(path) as f:
                content = f.read()
            t = content.replace(from_string, to_string)
            if t != content:
                with open(path, 'wb') as f:
                    f.write(t)

run()
