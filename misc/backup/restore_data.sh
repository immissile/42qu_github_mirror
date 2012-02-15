#Usage ./restore_data.sh 2012_xxxxx
./backup_table.sh
mysql -u root -p42qu zpage < table_main.sql
mysql -u root -p42qu zpage < $1
