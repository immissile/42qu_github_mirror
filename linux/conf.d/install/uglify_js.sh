## clone the repository
PREFIX=/opt
mkdir -p $PREFIX 
cd $PREFIX
git clone git://github.com/mishoo/UglifyJS.git

## make the module available to Node
mkdir -p ~/.node_libraries/
cd /usr/lib/node
ln -s $PREFIX/UglifyJS/uglify-js.js

## and if you want the CLI script too:
mkdir -p /usr/bin
cd /usr/bin
ln -s $PREFIX/UglifyJS/bin/uglifyjs
