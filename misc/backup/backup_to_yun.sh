#!/bin/bash

BACKUP_PATH=work@vm-192-168-16-114.shengyun.grandcloud.cn:/mnt/42qu/backup/

rsync -avl  -e ssh /mnt/zpage_db/mysql $BACKUP_PATH 
rsync -avl  -e ssh /mnt/zpage $BACKUP_PATH 
