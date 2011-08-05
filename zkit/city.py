# -*- coding: utf-8 -*-
from earth import PLACE_L1, PLACE_GET_CITY_L1L2, PLACE_GET_CITY_L2L3, place_name, BIT_COUNTRY_LEN, BIT_COUNTRY 
PLACE_MUNI = (
       4295032832, #北京
       4295098368, #上海
       4295229440, #天津
       4295163904, #重庆
       4295294976, #香港
       4295360512  #澳门
        )

def city(code):
    if (code&BIT_COUNTRY) >> BIT_COUNTRY_LEN == 1:
        if code in PLACE_MUNI:
            return code
        elif code in PLACE_L1:
            return 0
        else:
            p1 = PLACE_GET_CITY_L1L2
            if p1.get(code):
                return p1[code]
            else:
                p2 = PLACE_GET_CITY_L2L3
                if p2.get(code):
                    return p2[code]
    else:
        return (code&BIT_COUNTRY) >> BIT_COUNTRY_LEN



#def place12 (dic):
#    d1 = dict((y,x) for x,y in dic.items())
#    d = {}
#    for i in d1.keys():
#        for u in i:
#            d[u]=d1[i]
#    return d


if __name__ == '__main__':
    print place_name(city(4295298560))
    from earth import BIT_COUNTRY_LEN, BIT_COUNTRY, COUNTRY_DICT 
    country = (4295298560&BIT_COUNTRY) >> BIT_COUNTRY_LEN
  #  print COUNTRY_DICT[country]
    # dit =  place12(PLACE_L2L3)
   # print 'PLACE_GET_CITY_L2L3 = {'
   # for i in dit.keys():
   #     print i,':',dit[i],','

   # print '}'


