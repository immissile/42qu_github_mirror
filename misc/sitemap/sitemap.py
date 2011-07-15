#!/usr/bin/env python
#coding:utf-8
from _env import PWD
from os.path import join
import types
from datetime import datetime
import gzip
from zkit.single_process import single_process


SITEMAP_INDEX = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</sitemapindex>
"""
SITEMAP_INDEX_ITEM = """
   <sitemap>
      <loc>http://%s/misc/sitemap/%s.gz</loc>
      <lastmod>%s+08:00</lastmod>
   </sitemap>
"""

SITEMAP_FILE = []

import sitemap_iter

def save(filename, ormiter, seq=1):
    f = "%s_%s"%(filename, seq)
    SITEMAP_FILE.append(f)

    f = join(PWD, "file", f)
    ft = f+".txt"

    is_over = True
    with open(ft, "w") as output:
        for c, i in enumerate(ormiter):
            output.write("%s\n"%(i))
            if c > 49990:
                is_over = False
                break

    with open(ft, "rb") as output:
        with open('%s.gz'%f, "wb") as gzfile:
            f_out = gzip.GzipFile(filename="sitemap.txt", fileobj=gzfile)
            f_out.writelines(output)
            f_out.close()

    if is_over is False:
        save(filename, ormiter, seq+1)

@single_process
def run():
    for k, v in vars(sitemap_iter).iteritems():
        if type(v) is types.FunctionType and k.startswith("sitemap_"):
            k = k[8:]
            save(k, v())


    NOW = datetime.now().isoformat()[:19]
    with open(join(PWD, "file", "sitemap.xml"), "w") as index:
        index.write(
            SITEMAP_INDEX%(
                "".join(SITEMAP_INDEX_ITEM%(DOMAIN, i, NOW) for i in SITEMAP_FILE)
            )
        )

if __name__ == "__main__":
    run()


