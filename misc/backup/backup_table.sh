#!/bin/bash
PREFIX=$(cd "$(dirname "$0")"; pwd)
cd $PREFIX
python backup_table.py
sleep 2
cat table_main| sed 's/ AUTO_INCREMENT=[0-9]*\b//' >  table_main.sql
cat table_google| sed 's/ AUTO_INCREMENT=[0-9]*\b//' >  table_google.sql
rm table_main
rm table_google
