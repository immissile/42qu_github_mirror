#!/bin/bash

BACKUP_PATH=work@vps.42qu.me:/mnt/42qu/backup/

nohup rsync -avl  -e ssh  $BACKUP_PATH/zpage  /mnt &
