easy_install weberror
easy_install dbutils
easy_install pyrex
svn checkout http://python-libmemcached.googlecode.com/svn/trunk/ python-libmemcached-read-only 
cd python-libmemcached-read-only 
python setup.py install
easy_install hmako
easy_install mako 
easy_install cherrypy
easy_install https://github.com/facebook/tornado/tarball/master
easy_install https://github.com/earl/beanstalkc/tarball/master
