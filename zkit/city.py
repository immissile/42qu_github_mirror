# -*- coding: utf-8 -*-
from earth import PLACE_L1, PLACE_GET_CITY_L1L2, PLACE_GET_CITY_L2L3, place_name, BIT_COUNTRY_LEN, BIT_COUNTRY, BIT_COUNTRY_PROVINCE_CITY 

PLACE_MUNI = (
   4295032832, #北京
   4295098368, #上海
   4295229440, #天津
   4295163904, #重庆
   4295294976, #香港
   4295360512, #澳门
)

def city(code):
    if (code&BIT_COUNTRY) >> BIT_COUNTRY_LEN == 1:
        code = code&BIT_COUNTRY_PROVINCE_CITY
        if code in PLACE_MUNI:
            return code
        elif code in PLACE_L1:
            return 0
        else:
            if code in PLACE_GET_CITY_L1L2:
                return PLACE_GET_CITY_L1L2[code]
            else:
                if code in PLACE_GET_CITY_L2L3:
                    return PLACE_GET_CITY_L2L3[code]
    else:
        return code 





if __name__ == '__main__':
    print place_name(city(4699586560))
    print place_name(city(4497866752))
