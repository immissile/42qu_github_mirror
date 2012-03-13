
cd ~/zpage/config/
python make_dev_config.py
python nginx.py

cd ~/zpage/config/user
hg add .
hg commit -m"add user config"
hg fetch
hg push

sudo /etc/init.d/nginx reload


