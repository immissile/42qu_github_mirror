pre_last_time = 0
pre_line = 0
from collections import defaultdict
import datetime

min_count = defaultdict(int)
begin_time = 41000



with open('42qu_com_zsite.access_log') as log42qu:
    for pos , line in enumerate(log42qu):
        if pos < begin_time or pos > begin_time+700:
            continue

        line = line.strip()
        log_line = line.split(' ', 8)[:7]
        last_time = float(log_line[-1])
        diff = last_time - pre_last_time
        if pre_line:
            dt = str(datetime.datetime.fromtimestamp(last_time))
            pre_dt = str(datetime.datetime.fromtimestamp(pre_last_time))
            if dt[11:17] != pre_dt[11:17]:
                print ''
            url = pre_line.split('"')[-2].split()
            code = int(pre_line.split()[2])
            if code not in (200,302,404,304,301):
                print dt[11:19], code, 'http://%s%s'%(pre_line.split()[1], url[1]), url[0]

        pre_last_time = last_time
        pre_line = line
        min_count[int(last_time/60)] += 1


#for k, v in sorted(min_count.iteritems(), key=lambda x:x[0]):
#    print datetime.datetime.fromtimestamp(k*60), v
