#coding:utf-8

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, Model, McCacheM, McCacheA
from model.zsite import Zsite

def site_rec(user_id):
    return Zsite.mc_get(129) 
