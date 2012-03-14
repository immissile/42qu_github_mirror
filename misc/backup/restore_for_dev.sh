#!/bin/bash

DB=2012_03_12_03_20_01
DBPATH=~/data

mkdir -p $DBPATH
#scp work@42qu.com:/mnt/zpage_db/mysql/$DB.7z ~/data


#mysql -uzpage -p42qudev zpage < table_main.sql
#mysql -uzpage -p42qudev zpage_google < table_google.sql
 

cd $DBPATH
#7za x $DB.7z 
#mysql -uzpage -p42qudev zpage < $DB
#rm $DB

sudo /etc/init.d/redis stop
scp work@42qu.com:/var/lib/redis/dump.rdb  $DBPATH/dump.rdb
sudo mv  $DBPATH/dump.rdb /var/lib/redis/dump.rdb
sudo chown redis:redis /var/lib/redis/dump.rdb
sudo /etc/init.d/redis start

python restore_for_dev.py
