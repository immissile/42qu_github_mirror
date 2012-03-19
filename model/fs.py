import _env
from config import FILE_PATH, FILE_URL
from cid import CID_AUDIO
from os.path import join, exists, dirname
from os import remove, makedirs
from cStringIO import StringIO
from config import SITE_URL
import traceback

def fs_path(root, prefix, id, suffix):
    path = join(root, str(prefix), str(int(id)%1024), '%s.%s'%(id, suffix))
    return path

def fs_file(prefix, id, suffix):
    return fs_path(FILE_PATH, prefix, id, suffix)

def fs_url(prefix, id, suffix, url=FILE_URL):
    return fs_path(url, prefix, id, suffix)

def img2str(image, quality=95):
    f = StringIO()
    try:
        image = image.convert('RGB')
    except:
        traceback.print_exc()
    try:
        image.save(f, 'JPEG', quality=quality)
        return f.getvalue()
    except:
        traceback.print_exc()
    return ''

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

def fs_file_audio(key):
    return fs_file('mp3', key, 'exe')

def fs_url_audio(key, xsrf):
    return fs_url('wav', key, xsrf, SITE_URL)

def fs_set_audio(prefix, key, audio):
    fs_set(prefix, key, 'exe', audio)

