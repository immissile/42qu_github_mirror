#from model.user_session import user_id_by_base64
#from config import SITE_DOMAIN
#import re
SITE_DOMAIN='silegon.xxx'

def txt_wrap_by(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def erank():
    LOG_FILE_PATH = '/var/log/nginx/silegon_xxx_main.access_log'
    f = open(LOG_FILE_PATH, 'rb')
    file_content = f.read()
    f.close()
    access_result = []
    log_lines = file_content.split('\n')[0:-1]
    for log in log_lines:
        elements = log.split()
        site_url = elements[7]
        user_id_base64 = elements[-1]
        person_url = txt_wrap_by('"http://', SITE_DOMAIN, site_url)
        if person_url and user_id_base64 != '-' and person_url != 'god.':
            access_result.append(person_url+user_id_base64)
    return access_result


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
    result = erank()
    presult = single_sort(result)
    print presult

