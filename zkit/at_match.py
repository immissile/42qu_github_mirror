# -*- coding: utf-8 -*-

from pinyin import startswith_pinyin_initial
from pinyin import pinyin_by_str
from algorithm.unique import unique

def key_match(key, kvdict):
# start_result, contain_result
    s_result = []
    c_result = []

    for name, id in kvdict.iteritems():
        pos = name.find(key)
        if pos < 0:
            continue
        if pos == 0:
            t = s_result
        else:
            t = c_result
        t.append(id)

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

    s_result = []
    s_set = set()
    c_result = []

    if not key:
        return []

    if key.replace('-', '').isalnum():
        _s_result, _c_result = key_match(key, url_dict)
        s_result.extend(_s_result)
        c_result.extend(_c_result)
        s_set.update(_s_result)

    if len(s_set) < limit:
        _s_result_list, _c_result_list = key_match(
            key,
            dict(
                (k.lower(), v) for k, v in name_dict.iteritems()
            )
        )
        for _s_result in _s_result_list:
            s_result.extend(_s_result)
            s_set.update(_s_result)
        for _c_result in _c_result_list:
            c_result.extend(_c_result)

    if len(s_set) < limit:
        if key.isalpha() and key.lower():
            if len(key) == 1:
                _s_result_list = start_pin_match(key, name_dict)
            else:
                _s_result_list, _c_result_list = key_match(key, name_to_pinyin(name_dict))
                for _c_result in _c_result_list:
                    c_result.extend(_c_result)

            for _s_result in _s_result_list:
                s_result.extend(_s_result)
                s_set.update(_s_result)


    s_result = unique(s_result)
    len_s_result = len(s_result)

    while len_s_result < limit:
        for i in c_result:
            if i not in s_set:
                s_result.append(i)
                s_set.add(i)
                len_s_result += 1

        break

    if len_s_result > limit:
        s_result = s_result[:limit]

    return s_result


if __name__ == '__main__':
    name_dict = {
        '张沈鹏':[10001, 3]
    }
    url_dict = {
        'xzuroc':10001,
        'zhendi':10002,
        'kingli':10003,
        'realfex':10004
    }
    print zsite_by_key('peng', name_dict, url_dict, 4)
    print zsite_by_key('z', name_dict, url_dict, 4)
    print zsite_by_key('zu', name_dict, url_dict, 4)
