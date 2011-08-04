# -*- coding: utf-8 -*-
from earth import PLACE_L1, PLACE_GET_CITY_L1L2, PLACE_GET_CITY_L2L3 

def city(code):
    if code in PLACE_L1:
        return code
    else:
        p1 = PLACE_GET_CITY_L1L2
        if p1.get(code):
            return p1[code]
        else:
            p2 = PLACE_GET_CITY_L2L3
            if p2.get(code):
                return p2[code]



#def place12 (dic):
#    d1 = dict((y,x) for x,y in dic.items())
#    d = {}
#    for i in d1.keys():
#        for u in i:
#            d[u]=d1[i]
#    return d


if __name__ == '__main__':
    print city(4429250560)
   
    # dit =  place12(PLACE_L2L3)
   # print 'PLACE_GET_CITY_L2L3 = {'
   # for i in dit.keys():
   #     print i,':',dit[i],','

   # print '}'


