PREFIX=$(cd "$(dirname "$0")"; pwd)
crontab -l > $PREFIX/crontab
cd $PREFIX
#hg commit -m"auto crontab -l backup"
