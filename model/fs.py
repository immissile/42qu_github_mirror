import _env
from config import PIC_PATH, PIC_URL
from os.path import join, exists, dirname
from os import remove, makedirs
from cStringIO import StringIO

def fs_path(root, prefix, id, suffix):
    path = join(root, str(prefix), str(id%1024), '%s.%s'%(id, suffix))
    return path

def fs_file(prefix, id, suffix):
    return fs_path(PIC_PATH, prefix, id, suffix)

def fs_url(prefix, id, suffix):
    return fs_path(PIC_URL, prefix, id, suffix)

def img2str(image, quality=95):
    f = StringIO()
    image = image.convert('RGB')
    image.save(f, 'JPEG', quality=quality)
    return f.getvalue()

def fs_set(prefix, id, suffix, data):
    path = fs_file(prefix, id, suffix)
    dirpath = dirname(path)
    if not exists(dirpath):
        makedirs(dirpath)
    f = open(path, 'wb')
    f.write(data)
    f.close()

def fs_get_jpg(prefix, key):
    f = fs_file_jpg(prefix, key)
    if exists(f):
        with open(f) as infile:
            return infile.read()

def fs_set_jpg(prefix, key, image, quality=95):
    fs_set(prefix, key, 'jpg', img2str(image, quality))

def fs_file_jpg(prefix, key):
    return fs_file(prefix, key, 'jpg')

def fs_url_jpg(prefix, key):
    return fs_url(prefix, key, 'jpg')

#print fs_file("test", 1, "jpg")
#print fs_link("test", 1, "jpg")
#import init_env
#from base64 import urlsafe_b64encode, urlsafe_b64decode
#from myconf.config import KV_HOST, KV_PATH
#from mmhash import get_unsigned_hash
#from cStringIO import StringIO
#from shutil import move
#
#
#
#
#def fs_get(prefix, key):
#    p = get_path(KV_PATH, prefix, key)
#    if exists(p):
#        f = open(p, "rb")
#        r = f.read()
#        f.close()
#        return r
#
#def fs_set_jpg_id_ver_incr_mv(prefix, id, ver):
#    prekey = "%s.%s.jpg"%(id, int(ver)-1)
#    key = "%s.%s.jpg"%(id, ver)
#    fs_mv(prefix, prekey, key)
#
#def fs_mv(prefix, prekey, key):
#    op = get_path(KV_PATH, prefix, prekey)
#    if exists(op):
#        np = get_path(KV_PATH, prefix, key)
#        makepathdirs(np)
#        move(op, np)
#
#
#def fs_set_jpg_id_ver(prefix, id, ver, data):
#    key = "%s.%s.jpg"%(id, ver)
#    fs_set_jpg(prefix, key, data)
#
#def fs_get_jpg_id_ver(prefix, id, ver):
#    key = "%s.%s.jpg"%(id, ver)
#    return fs_get(prefix, key)
#
#def fs_url_jpg_id_ver(prefix, id, ver):
#    key = "%s.%s.jpg"%(id, ver)
#    return get_path(KV_HOST, prefix, key)
#
#def fs_rm(prefix, key):
#    p = get_path(KV_PATH, prefix, key)
#    if exists(p):
#        remove(p)
#
#def fs_set_jpg(prefix, key, image, quality=90):
#    fs_set(prefix, key, img2str(image, quality))
#
#def fs_url(prefix, key):
#    return get_path(KV_HOST, prefix, key)
#
#def img2str(image, quality=95):
#    f = StringIO()
#    image = image.convert('RGB')
#    image.save(f, 'JPEG', quality=quality)
#    return f.getvalue()
#
#
