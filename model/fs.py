import _env
from config.zpage_host import STATIC_PATH
from os.path import join, exists, dirname
from os import remove, makedirs

def get_path(prefix, id):
    path = join(STATIC_PATH, prefix, id%1024)
    if not exists(path):
        makedirs(path)
    path = join(path, key)
    return path


class Fs(object):
    def __init__(self, prefix):
        pass

    def get(self, id):
        pass

    def set(self, id, value):
        pass

    def link(self, id):
        pass


#import init_env
#from base64 import urlsafe_b64encode, urlsafe_b64decode
#from myconf.config import KV_HOST, KV_PATH
#from mmhash import get_unsigned_hash
#from cStringIO import StringIO
#from shutil import move
#
#
#
#def fs_set(prefix, key, data):
#    path = get_path(KV_PATH, prefix, key)
#    makepathdirs(path)
#    f = open(path, "wb")
#    f.write(data)
#    f.close()
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
