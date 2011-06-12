python backup_table.py
table=table_main.sql
cat $table| sed 's/ AUTO_INCREMENT=[0-9]*\b//' > $table 
