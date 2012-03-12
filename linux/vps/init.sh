cd ~
if [  -f ~/.ssh/id_rsa.pub ]; then
echo "~/.ssh/id_rsa.pub exist"
else 
ssh-keygen -t rsa -f ~/.ssh/id_rsa -P "" -q;
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys;
fi

virtualenv .env
