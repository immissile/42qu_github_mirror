wget -c http://launchpad.net/libmemcached/1.0/0.40/+download/libmemcached-0.40.tar.gz
tar zxf libmemcached-0.40.tar.gz

cd libmemcached-0.40
patch -p1 < ../python-libmemcached/patches/empty_string.patch
patch -p1 < ../python-libmemcached/patches/buffer_requests.patch 
patch -p1 < ../python-libmemcached/patches/fail_over.patch
./configure
make
sudo make install
cd ..

cd  python-libmemcached ; 
python setup.py build
sudo python setup.py install
