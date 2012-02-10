mkdir -p /mnt/zpage_db/redis
FILEDIR=/mnt/zpage_db/redis
FILE=$FILEDIR/`date +%Y_%m_%d_%H_%M_%S`.7z
7z a $FILE /var/lib/redis 
