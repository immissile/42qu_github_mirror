#!/bin/bash

BACKUP_PATH=work@vps.42qu.me:/mnt/42qu/backup/

rsync -avl  -e ssh /mnt/zpage_db/mysql $BACKUP_PATH 
rsync -avl  -e ssh /mnt/zpage $BACKUP_PATH 
