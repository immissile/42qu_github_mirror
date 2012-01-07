pre_last_time = 0
pre_line = 0
from collections import defaultdict
import datetime
import pylzma

min_count = defaultdict(int)
begin_time = 41000


logfile = """
/var/log/nginx_backup/42qu_com_zsite.access_log-20111231.lzma
/var/log/nginx_backup/42qu_com_zsite.access_log-20120101.lzma
/var/log/nginx_backup/42qu_com_zsite.access_log-20120102.lzma
/var/log/nginx_backup/42qu_com_zsite.access_log-20120103.lzma
/var/log/nginx_backup/42qu_com_zsite.access_log-20120104.lzma
/var/log/nginx_backup/42qu_com_zsite.access_log-20120105.lzma
/var/log/nginx_backup/42qu_com_zsite.access_log-20120106.lzma
/var/log/nginx_backup/42qu_com_zsite.access_log-20120107.lzma
/var/log/nginx_backup/42qu_com_zsite.access_log-20120108.lzma
""".strip().split()
import lzma



def error499_count(data):
    count = 0
    for pline in data.split("\n"):
        line = pline.split()
        if len(line)<3:
            continue
        code = int(line[2])
        if code == 499:
            count += 1
    return count

for line in logfile:
    with open(line) as nginxlog:
        data = lzma.decompress(nginxlog.read())
    print line,error499_count(data)
