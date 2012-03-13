hg commit -m"vps new"
hg fetch

python vps_new.py

cd ~/zpage/config/
python make_dev_config.py
python nginx.py

cd ~/zpage/config/user
hg add .
hg commit -m"add user config"
hg push

sudo /etc/init.d/nginx reload


