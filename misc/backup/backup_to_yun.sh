#!/bin/bash


rsync -avl  -e ssh /mnt/zpage  work@vm-192-168-16-114.shengyun.grandcloud.cn:/mnt/42qu/backup/zpage
rsync -avl  -e ssh /mnt/zpage_db/mysql  work@vm-192-168-16-114.shengyun.grandcloud.cn:/mnt/42qu/backup/mysql
