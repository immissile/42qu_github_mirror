pre_last_time = 0
pre_line = 0
from collections import defaultdict
import lzma

min_count = defaultdict(int)
begin_time = 41000
import glob

logfile = """/var/log/nginx_backup/42qu_com_zsite.access_log-*.lzma"""



def error499_count(data):
    count = 0
    for pline in data.split('\n'):
        line = pline.split()
        if len(line) < 3:
            continue
        code = int(line[2])
        if code == 499:
            count += 1
    return count

for line in sorted(glob.glob(logfile))[-30:]:
    with open(line) as nginxlog:
        data = lzma.decompress(nginxlog.read())
    print line, error499_count(data)
