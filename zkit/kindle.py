#coding:utf-8
#from os.path import abspath, dirname, join
#from os import walk, remove
#from hashlib import md5
#import traceback
#import codecs
#
#def encode_utf8(txt):
#    try:
#        txt = txt.decode('gb18030').encode('utf-8')
#    except:
#        pass
#    if txt[:3] == codecs.BOM_UTF8:
#        txt = txt[3:]
#    return txt
#
#def style_txt(txt):
#    txt = '\n\n'.join(filter(bool,
#        map(
#            str.strip, txt.replace("　"," ").replace(""," ").replace(""," ").split("\n") 
#        )
#    ))
#    return txt
#
#path = abspath(dirname(__file__))
#
#exist = set()
#
#for root, dirs, files in walk(path):
#    for file in files:
#        if file.lower().endswith('.txt'):
#            path = join(root, file)
#            with open(path, 'rb') as f:
#                oldtxt = f.read().strip())
#                txt = encode_utf8(style_txt(oldtxt))
#                hash = md5(txt).digest()
#
#            if hash in exist:
#                print path
#                remove(path)
#                continue
#
#            exist.add(hash)
#
#
#            if txt != oldtxt:
#                with open(path, 'wb') as f:
#                    f.write(txt)
#
#
#
