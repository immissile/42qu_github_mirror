#!/usr/bin/env python
#coding:utf-8

def mc_func_get_dict_with_key_pattern(mc, func, key_list, key_pattern):
    t = mc.get_dict(key_pattern%i for i in key_list)
    result = {}
    for i in key_list:
        key = key_pattern%i
        o = t[key]
        if o is None:
            o = func(*i)
        result[i] = o
    return result

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
