cp vimrc /etc/vim/vimrc
cp vim/* /usr/share/vim/vimfiles/ -R
cp sudoers /etc/sudoers
cp deltmp /usr/bin
cd pythius
python setup.py install
cd ..
