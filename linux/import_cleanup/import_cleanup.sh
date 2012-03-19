PREFIX=$(cd "$(dirname "$0")"; pwd)
pyflakes . > out.flakes
python $PREFIX/import_cleanup.py

