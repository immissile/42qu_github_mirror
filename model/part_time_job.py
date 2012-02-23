#coding:utf-8


from _db import Model, McNum
from time import time

PART_TIME_JOB_CID_FEED_IMPORT = 1 

class PartTimeJob(Model):
    pass

def part_time_job_new(cid, rid, user_id):
    record = PartTimeJob.get_or_create(cid=cid, rid=rid, user_id=user_id)
    record.create_time = int(time())
    record.save()

    part_time_job_count_by_cid.delete(cid)

part_time_job_count_by_cid = McNum(
    lambda cid:PartTimeJob.where(cid=cid).count(),
    "PartTimeJobCountByCid:%s"
)


def id_list_by_part_time_job_cid(cid, limit, offset):
    rid_list = PartTimeJob.where(cid=cid).order_by("id desc").col_list(limit, offset, "rid, user_id")
    return rid_list

if __name__ == "__main__":
    pass
    cid = PART_TIME_JOB_CID_FEED_IMPORT
    limit = 10
    offset = 0
    print part_time_job_count_by_cid(cid)
    print id_list_by_part_time_job_cid(cid, limit, offset)

