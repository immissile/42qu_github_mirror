import init_env
from config import SITE_DOMAIN
#from model.zsite import Zsite
from model.user_session import user_id_by_base64
from model.zsite_link import id_by_url
from model.zsite_date import now_days
from model._db import Model


class ZsiteUvDaily(Model):
    pass

def write_user_conern_to_model(presult):
    today = now_days()
    pre_user_id = None
    count = 0
    for item in presult:
        user_url, visitor = item.split('.')
        if user_url.isdigit():
            user_id = user_url
        else:
            user_id = id_by_url(user_url)
        if pre_user_id == None or user_id == pre_user_id:
            count += 1
        else:
            uv_daily = ZsiteUvDaily(
                           zsite_id=pre_user_id,
                           uv=count,
                           days=today
                       )
            uv_daily.save()
            count = 0
        pre_user_id = user_id



SUFFIX_LEN = len(SITE_DOMAIN)+1

def erank(path):
    with open(path) as infile:
        for log in infile:
            user_id_base64, domain, other = log.split(" ", 2)
            person_url =  domain[:SUFFIX_LEN]
            print person_url, user_id_base64 
            if person_url and user_id_base64 != '-':
                yield user_id_by_base64(user_id_base64), domain

def single_sort(result):
    pre_value = None
    presult = []
    result.sort()
    for value in result:
        if value == pre_value:
            continue
        pre_value = value
        presult.append(value)
    return presult


if __name__ == '__main__':
    LOG_FILE_PATH = '/var/log/nginx/silegon_xxx_main.access_log'
    for uid, domain in erank(LOG_FILE_PATH):
        print uid, domain
    raise
    presult = single_sort(result)
    write_user_conern_to_model(presult)
    print presult

