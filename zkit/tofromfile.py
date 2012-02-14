#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshal import dumps, loads
from gzip import GzipFile

def tofile(f , obj):
    out = GzipFile(f, 'wb')
    out.write( dumps(obj) )
    out.close()

def fromfile(f):
    infile = GzipFile(f)
    result = loads(infile.read())
    infile.close()
    return result



if __name__ == '__main__':
    tofile('z', {2:2})
    print fromfile("z")
