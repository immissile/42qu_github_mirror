filename=2012_02_27_12_12_19
scp work@42qu.com:/mnt/zpage_db/mysql/$filename.7z .
7za x $filename.7z
mysql -uroot -p42qu zpage < table_main.sql
mysql -uroot -p42qu zpage < $filename


