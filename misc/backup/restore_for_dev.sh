#!/bin/bash

DB=2012_03_12_03_20_01


mkdir -p ~/data
#scp work@42qu.com:/mnt/zpage_db/mysql/$DB.7z ~/data


#mysql -uzpage -p42qudev zpage < table_main.sql
#mysql -uzpage -p42qudev zpage_google < table_google.sql
 

cd ~/data
#7za x $DB.7z 
mysql -uzpage -p42qudev zpage < $DB
rm $DB
 
