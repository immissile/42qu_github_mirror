#coding:utf-8
from _db import Model, McModel
from time import time

TAG_EXP_ADMIN_STATE_REJECT = 5
TAG_EXP_ADMIN_STATE_INIT = 10
TAG_EXP_ADMIN_STATE_ACCEPT = 15

class TagExp(Model):
    pass

class TagExpAdmin(Model):
    pass

def tag_exp_admin_new(user_id, tag_id, tag_exp_id):
    #TODO 先 select id 检查是否有未审核的 , 如果有update它的state , 如果没有 就insert新的
    c = TagExpAdmin.raw_sql("..... limit 1", )
    id = c.fetchone()
    if id:
        id = id[0]
        c = TagExpAdmin.raw_sql()
    else:
        c = TagExpAdmin.raw_sql()

    return c.lastrowid

def tag_exp_admin_accept(tag_exp_admin_id):
    _tag_exp_admin_state_set(tag_exp_admin_id, TAG_EXP_ADMIN_STATE_ACCEPT)

def tag_exp_admin_reject(tag_exp_admin_id):
    _tag_exp_admin_state_set(tag_exp_admin_id, TAG_EXP_ADMIN_STATE_REJECT)

def _tag_exp_admin_state_set(tag_exp_admin_id, state):
    #TODO
    pass
    
def tag_exp_txt_by_user_id_tag_id(user_id, tag_id):
    #TODO
    return ""

def tag_exp_new_apply_for_admin(user_id, tag_id, txt):
    tag_exp_id = tag_exp_new(user_id, tag_id, txt)
    tag_exp_admin_new(user_id, tag_id, tag_exp_id)

def tag_exp_new(user_id, tag_id, txt):
    now = time()
    c = TagExp.raw_sql(
        "insert into tag_exp (user_id, tag_id, txt, time) values (%s,%s,%s,%s) on duplicate key update txt=%s, time=%s",
        user_id, tag_id, txt, now, txt, now
    )
    id = c.lastrowid
    return id

if __name__ == "__main__":
    #c = TagExp.raw_sql("select count(1) from tag_exp")
    #c.fetchone()
    #user_id = 1
    #tag_id = 2
    #print tag_exp_new(user_id, tag_id, "zsp331245t6yuzzzzzzzzzzzzzzzzzzzz")

