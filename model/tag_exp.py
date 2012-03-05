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

def tag_exp_admin_new( tag_id, tag_exp_id):
    #TODO 先 select id 检查是否有未审核的 , 如果有update它的state , 如果没有 就insert新的
    o = TagExpAdmin.get_or_create(
        tag_exp_id=tag_exp_id, 
        tag_id=tag_id
    )
    if not \
            o.state\
       or\
            o.state<TAG_EXP_ADMIN_STATE_ACCEPT:
        o.state = TAG_EXP_ADMIN_STATE_INIT
    o.save() 
    return o.id 

def tag_exp_admin_accept(tag_exp_admin_id):
    _tag_exp_admin_state_set(tag_exp_admin_id, TAG_EXP_ADMIN_STATE_ACCEPT)

def tag_exp_admin_reject(tag_exp_admin_id):
    _tag_exp_admin_state_set(tag_exp_admin_id, TAG_EXP_ADMIN_STATE_REJECT)

def _tag_exp_admin_state_set(tag_exp_admin_id, state):
    #TODO
    pass
    
def tag_exp_state_txt_by_user_id_tag_id(user_id, tag_id):
    c = TagExp.raw_sql(
        "select id, txt from tag_exp where user_id=%s and tag_id=%s limit 1",
        user_id, tag_id
    )
    r = c.fetchone()
    if r is None:
        txt = ''
        id = 0
    else:
        id , txt = r

    if id: 
        state = TagExpAdmin.raw_sql(
            "select state from tag_exp_admin where tag_exp_id=%s limit 1",
            id
        )
        r = c.fetchone()
        if r is None:
            state = 0
        else:
            state = r[0]
            #print state , "!!!!!!"
    else:
        state = 0 
    
    return [state, txt]

def tag_exp_new_apply_for_admin(user_id, tag_id, txt):
    tag_exp_id = tag_exp_new(user_id, tag_id, txt)
    tag_exp_admin_new(tag_id, tag_exp_id)

def tag_exp_new(user_id, tag_id, txt):
    now = time()
    c = TagExp.raw_sql(
        "insert into tag_exp (user_id, tag_id, txt, time) values (%s,%s,%s,%s) on duplicate key update txt=%s, time=%s",
        user_id, tag_id, txt, now, txt, now
    )
    id = c.lastrowid
    return id

if __name__ == "__main__":
    ##c = TagExp.raw_sql("select count(1) from tag_exp")
    ##c.fetchone()
    user_id = 2
    tag_id = 6
    tag_exp_new(user_id, tag_id, "huhuchen")

