PREFIX=$(cd "$(dirname "$0")"; pwd)
mkdir -p /mnt/$USER/mysql
FILEDIR=/mnt/$USER/mysql
FILE=$FILEDIR/`date +%Y_%m_%d_%H_%M_%S`.7z
python $PREFIX/backup_data.py | 7z a -si -bd  $FILE > /dev/null


#scp $FILE work@pc4.stdyun.com:/home/work/backup/mysql_daily/
#rsync -aSvH /fdist1/qu/qufs/* work@pc4.stdyun.com:/mnt/file/42qu/nginx/ > /dev/null
#python $PREFIX/backup_data.py | 7z a -si -bd /mnt/sb/backup/mysql.`date +%Y_%m_%d_%H_%M_%S`.7z > /dev/null
