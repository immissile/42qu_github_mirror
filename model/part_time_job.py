#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import Model
from time import time

class PartTimeJob(Model):
    pass

def part_time_job_new(cid,rid,user_id):
    record = PartTimeJob.get_or_create(cid=cid, rid=rid, user_id=user_id)
    record.create_time = int(time()) 
    record.save()

if __name__ == '__main__':
    part_time_job_new(1,1,33)
