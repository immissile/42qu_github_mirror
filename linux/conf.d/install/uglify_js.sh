## clone the repository
mkdir -p /where/you/wanna/put/it
cd /where/you/wanna/put/it
git clone git://github.com/mishoo/UglifyJS.git

## make the module available to Node
mkdir -p ~/.node_libraries/
cd ~/.node_libraries/
ln -s /where/you/wanna/put/it/UglifyJS/uglify-js.js

## and if you want the CLI script too:
mkdir -p ~/bin
cd ~/bin
ln -s /where/you/wanna/put/it/UglifyJS/bin/uglifyjs
