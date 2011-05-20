#!/usr/bin/env python
#coding:utf-8

def mc_func_get_list(mc, func, key_list):
    t = mc.get_multi(key_list)
    r = []
    for i in key_list:
        o = t[i]
        if o is None:
            o = func(i)
        r.append(o)
    return r
