#!/usr/bin/env python
#coding:utf-8

def mc_func_get_list(mc, func, key_list):
    t = mc.get_dict(key_list)
    r = []
    for i in key_list:
        o = t[i]
        if o is None:
            o = func(i)
        r.append(o)
    return r

def mc_func_get_dict(mc, func, key_list):
    t = mc.get_dict(key_list)
    for i in key_list:
        if t[i] is None:
            t[i] = func(i)
    return t
