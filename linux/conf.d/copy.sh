cp vimrc /etc/vim/vimrc
cp vim/* /usr/share/vim/vimfiles/ -R
cp sudoers /etc/sudoers
cp bin/* /usr/bin
cp j2 /etc/bash/ -R
cp bashrc /etc/bash/bashrc
cd pythius
python setup.py install
cd ..
