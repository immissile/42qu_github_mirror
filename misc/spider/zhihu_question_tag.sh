rm  /mnt/zdata/train/tag/zhihu
python zhihu_question_tag.py
scp  -C -c blowfish  /mnt/zdata/train/tag/zhihu work@pc3.stdyun.com:/home/work/wanfang/zhihu
