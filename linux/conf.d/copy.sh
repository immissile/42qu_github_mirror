cp vimrc /etc/vim/vimrc
cp vim/* /usr/share/vim/vimfiles/ -R
cp sudoers /etc/sudoers
cp bin/* /usr/bin
cd pythius
python setup.py install
cd ..
