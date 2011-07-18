rm mysql.7z
scp work@pc4.stdyun.com:/mnt/zpage_db/mysql/mysql.7z .
7za x mysql.7z
mysql -uroot -p42qu zpage < table_main.sql
mysql -uroot -p42qu zpage < mysql
rm mysql
