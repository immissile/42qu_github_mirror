
PYTHONLIBPATH=/usr/lib/python2.6/site-packages/ 
mkdir -p memlink
touch memlink/__init__.py
cp *.py memlink/ 
cp *.so memlink/
rm $PYTHONLIBPATH/memlink -rf
mv memlink $PYTHONLIBPATH
