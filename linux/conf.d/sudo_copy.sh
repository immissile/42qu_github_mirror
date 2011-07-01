cp vimrc /etc/vim/vimrc
cp vim/* /usr/share/vim/vimfiles/ -R
cp sudoers /etc/sudoers
cp bin/* /usr/bin
cp j2 /etc/bash/ -R
cp bashrc /etc/bash/bashrc
cp dnsmasq.conf /etc/dnsmasq.conf
mkdir -p /var/log/nginx_backup/
cp logrotate.d/* /etc/logrotate.d/ 
