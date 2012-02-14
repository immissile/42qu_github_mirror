#coding:utf-8


def starter_new(
    user_id,
    name,
    txt,
    cid,
    pid,
    pic_id,
    price,
    end_time,
):
#cid
#设计
#旅行
#影视
#摄影
#科技
#音乐
#人文
#出版
#其他
    pass
    #return zsite


def starter_active(id):
    pass

def starter_reject(id):
    pass

def starter_renew(id):
    pass


class Starter:
    def starter_can_admin(self, user_id):
        pass

    def end(self):
        pass

def starter_id_list_user_id_state(user_id, state):
    pass

def starter_list_user_id_state(user_id, state):
    pass

def starter_count_user_id_state(user_id, state):
    pass

def starter_count_list_user_id_state(user_id, state):
    pass



def starter_list_order_by_end_time(state, offset, limit):
    pass

def starter_id_list_order_by_end_time(state, offset, limit):
    pass



def starter_list_order_by_id(state, offset, limit):
    pass

def starter_id_list_order_by_id(state, offset, limit):
    pass



def starter_sell_new(starter_id, txt, cid, price, buy_max):
    pass

def starter_buy_new(starter_sell_id, user_id, state, buy_address_id):
    pass

def buy_address_new(user_id , receiver , pid , address , zipcode , phone_list , state):
    pass

def starter_buy_state(starter_buy_id, state):
    pass



def starter_sell_id_list_by_starter_id(starter_id):
    pass

def starter_sell_list_by_starter_id(starter_id):
    pass



def starter_buy_id_list_by_user_id(user_id):
    pass

def starter_buy_list_by_user_id(user_id):
    pass



def starter_buy_id_list_by_sell_id(starter_sell_id):
    pass

def starter_buy_list_by_sell_id(starter_sell_id):
    pass



def starter_buy_count_by_starter_id_state(starter_id, state):
    pass

def starter_buy_id_list_by_starter_id_state(starter_id, state):
    pass

def starter_buy_list_by_starter_id_state(starter_id, state):
    pass


def starter_buy_reply_new(starter_buy_id, user_id, txt):
    pass

def starter_scan_end():
    pass


#TODO 发布公告 (邮件通知可选)


if __name__ == '__main__':
    pass



