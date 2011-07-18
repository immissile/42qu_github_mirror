PREFIX=$(cd "$(dirname "$0")"; pwd)
mkdir -p /mnt/zpage_db/mysql
FILEDIR=/mnt/zpage_db/mysql
FILE=$FILEDIR/mysql.7z
rm $FILE
python $PREFIX/backup_data.py | 7z a -si -bd $FILE > /dev/null
cp $FILE $FILEDIR/`date +%Y_%m_%d_%H_%M_%S`.7z


#scp $FILE work@pc4.stdyun.com:/home/work/backup/mysql_daily/
#rsync -aSvH /fdist1/qu/qufs/* work@pc4.stdyun.com:/mnt/file/42qu/nginx/ > /dev/null
#python $PREFIX/backup_data.py | 7z a -si -bd /mnt/sb/backup/mysql.`date +%Y_%m_%d_%H_%M_%S`.7z > /dev/null
