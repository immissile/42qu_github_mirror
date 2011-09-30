# -*- coding: utf-8 -*-

from pinyin import startswith_pinyin_initial
from pinyin import pinyin_by_str
from algorithm.unique import unique

name_dict = {
    "张沈鹏":10001,
    }
url_dict = {
    "zuroc":10001,
    "zhendi":10002,
    "kingli":10003,
    "realfex":10004
}
def key_match(key, kvdict):
# start_result, contain_result
    s_result = []
    c_result = []
    
    for name, id in kvdict.iteritems():
        pos = name.find(key)
        if pos<0:
            continue
        if pos==0:
            s_result.append(id)
        else:
            c_result.append(id)
    return s_result, c_result

def start_pin_match(key, kvdict):
    s_result = []
    for name, id in kvdict.iteritems():
        if startswith_pinyin_initial(key)(name):
            s_result.append(id)
    return s_result

def name_to_pinyin(name_dict):
    pinyin = dict()
    for name, id in name_dict.iteritems():
        pinyin[pinyin_by_str(name)] = id
    return pinyin

def zsite_by_key(key, name_dict, url_dict, limit):
        
    s_result =[]
    c_result = []
    if key.replace("-","").isalnum():
        _s_result, _c_result = key_match(key, url_dict)
        s_result.extend(_s_result)
        c_result.extend(_c_result)

    if len(unique(s_result)) < limit:
        _s_result, _c_result = key_match(key, name_dict)
        s_result.extend(_s_result)
        c_result.extend(_c_result)
    
    if len(unique(s_result)) < limit:   
        if key.isalpha() and key.lower():
            if len(key) == 1:
                s_result.extend(start_pin_match(key, name_dict))
            else:
                _s_result, _c_result = key_match(key, name_to_pinyin(name_dict))
                s_result.extend(_s_result)
                c_result.extend(_c_result)
    if len(unique(s_result)) < limit:
        s_result.extend(c_result)

    if len(unique(s_result)) > limit:
        s_result = s_result[:limit]

    return unique(s_result)


if __name__ == '__main__':
    print zsite_by_key('peng',name_dict,url_dict,4)
