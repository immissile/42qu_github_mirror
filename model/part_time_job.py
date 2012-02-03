#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import Model
from time import time
from config import PART_TIME_JOBS_RULES,  PART_TIME_JOBS_PAGE_DICT

class PartTimeJob(Model):
    pass

def part_time_job_new(cid,rid,user_id):
    record = PartTimeJob.get_or_create(cid=cid, rid=rid, user_id=user_id)
    record.create_time = int(time()) 
    record.save()

def page_is_allowed_by_user_id_path(user_id,path):
    job_id_list = dict(PART_TIME_JOBS_RULES).get(user_id,[])
    allowed_path = set()
    for job_id in job_id_list:
        allowed_path|=set(PART_TIME_JOBS_PAGE_DICT[job_id])
    return path in allowed_path

if __name__ == '__main__':
    part_time_job_new(1,1,10001517)
