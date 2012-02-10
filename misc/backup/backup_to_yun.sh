#!/bin/bash

BACKUP_PATH=work@vps.42qu.me:/mnt/42qu/backup/

nohup rsync -avl  -e ssh /home/work/zpage $BACKUP_PATH/work/ &
nohup rsync -avl  -e ssh /mnt/zpage_db/mysql $BACKUP_PATH & 
nohup rsync -avl  -e ssh /mnt/zpage_db/redis $BACKUP_PATH & 
#nohup rsync -avl  -e ssh /mnt/zpage $BACKUP_PATH & 
