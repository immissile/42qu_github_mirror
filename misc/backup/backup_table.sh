#!/bin/sh
python backup_table.py
sleep 2
cat table_main| sed 's/ AUTO_INCREMENT=[0-9]*\b//' >  table_main.sql
