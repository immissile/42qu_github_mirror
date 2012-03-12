cd ~
if [  -f ~/.ssh/id_rsa.pub ]; then
echo "~/.ssh/id_rsa.pub exist"
else 
ssh-keygen -t rsa -f ~/.ssh/id_rsa -P "" -q;
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys;
fi

PREFIX=$(cd "$(dirname "$0")"; pwd)
cp -r PREFIX/config/. ~/ 

source ~/.bash_profile

virtualenv .env
pip install setuptools --upgrad


