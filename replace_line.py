#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath, dirname, basename, join
from os import walk

FROM_STRING = """
expires 0;
"""

TO_STRING = """
expires off;
"""

FROM_STRING = FROM_STRING.strip()
TO_STRING = TO_STRING.strip()

FILE = abspath(__file__)

for dirpath, dirnames, filenames in walk(dirname(FILE)):
    dirname = basename(dirpath)
    if dirname.startswith("."):
        continue

    for filename in filenames:
        suffix = filename.rsplit(".", 1)[-1]
        if suffix not in ("py", "htm", "txt","conf"):
            continue
        path = join(dirpath, filename)
        if path == FILE:
            continue
        with open(path) as f:
            content = f.read()
        t = content.replace(FROM_STRING, TO_STRING)
        if t != content:
            with open(path, "wb") as f:
                f.write(t)


