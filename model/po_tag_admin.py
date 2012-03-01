#coding:utf-8
from _db import Model, McModel

class TagExp(Model):
    pass

class TagExpAdmin(Model):
    pass

#Base=
#
#class Tag_exp(Base):
#    __tablename__ = "tag_exp"
#    user_id = 
#    tag_id = 
#    txt =
#    create_time = 
#
#    def __init__(self,user_id,tag_id,txt,create_time):
#        self.user_id = user_id
#        self.tag_id = tag_id
#        self.txt = txt
#        self.create_time = create_time
#
#    def edit_tag_exp_txt(cls,newtxt):
#        cls.txt = newtxt
#
#    def check_exist(cls,user_id,tag_id):
#        if cls.user_id == user_id and cls.tag_id == tag_id:
#            return True
#        else:
#            return False
#
#
#
#class Tag_exp_for_admin(Base):
#    __tablename__ = "tag_exp_for_admin"
#    tag_id =
#    tag_exp_id =
#    state = 
#    admin_id = 
#    create_time =
#
#    def __init__(self,tag_id,tag_exp_id,state = 10,admin_id = None,create_time):
#        self.tag_id = tag_id
#        self.tag_exp_id = tag_exp_id
#        self.create_time = create_time
#    
#    def _get_state(self):
#        return self.state
#
#    def edit_state(cls,admin_id,newstate):
#        cls.admin_id = int(admin_id)
#        cls.state = int(newstate)
#        
#    def check_exist(cls,tag_id,tag_exp_id):
#        if cls.tag_id == tag_id and cls.tag_exp_id == tag_exp_id:
#            return True
#        else:
#            return False
#
#
#
#
#if not (check_exist() and check_exist):
#    Tag_exp()
#    Tag_exp_for_admin()
#elif a._get_state == 10 and 表单内容不为空:
#    Tag_exp.edit_tag_exp_txt()
#elif a._get_state == 20 and 表单内容不为空:
#    已经被拒绝
#    Tag_exp()
#    Tag_exp_for_admin()
#else a._get_state == 30:
#    show somgthing
#        
