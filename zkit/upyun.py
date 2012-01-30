#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import base64
from urllib2 import urlopen
import httplib
import os
from fetch_pic import fetch_pic
from cStringIO import StringIO
from pic import pic_fit_width_cut_height_if_large
from hashlib import md5
import traceback
from config import UPYUN_USERNAME, UPYUN_PWD, UPYUN_SPACENAME, UPYUN_API_URL, UPYUN_DOMAIN, UPYUN_DIRNAME, UPYUN_PATH_BUILDER

class UpYun(object):
    def __init__(self, domain, username, password, spacename, headers={}):
        self.domain, self.username, self.password, self.headers, self.spacename = domain, username, password, headers, spacename
        self.headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (self.username, self.password))
        self.headers['Mkdir'] = 'true'

    def upload(self, filename):
        with open(filename) as f:
            data = f.read()
            self.upload_data(filename, data)

    def upload_data(self, path, data):
        path = os.path.join('/', self.spacename , os.path.basename(path))
        connection = httplib.HTTPConnection(UPYUN_API_URL)
        connection.request('PUT', path, data, self.headers)
        result = connection.getresponse()
        #print "DDDDDDDDDDD",result.status, result.reason,self.domain%os.path.basename(path)
        return self.get_file_url(os.path.basename(path))

    def upload_img(self, path, img):
        data = StringIO()
        img.save(data,'JPEG')
        url = self.upload_data(path,data.getvalue())
        data.close()
        return url
    
    def get_file_url(self,filename):
        return upyun_rsspic.domain%filename

def builder_path(suffix, url):
    filename = md5(url).hexdigest()+'.jpg'
    file_path = suffix%( '/'.join(filename[:2]))
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return os.path.join(file_path, filename), filename


def save_to_md5_file_name(suffix, data, url, root='/'):
    file_path, filename = builder_path(suffix, url)
    if not os.path.exists(file_path) and data:
        with open(file_path, 'w') as f:
            f.write(data)
    return file_path, filename


def exists(url):
    site, path = os.path.split(url)
    conn = httplib.HTTPConnection(site.replace('http://', ''))
    conn.request('HEAD', '/'+path)
    response = conn.getresponse()
    conn.close()
    return response.status == 200


upyun_rsspic = UpYun(UPYUN_DOMAIN, UPYUN_USERNAME, UPYUN_PWD, UPYUN_SPACENAME)

def upyun_fetch_pic(url):
    file_path, filename = builder_path(UPYUN_PATH_BUILDER, url)
    upyun_url = upyun_rsspic.domain%filename
    #print url,upyun_url
    if not os.path.exists(file_path):
        img = fetch_pic(url)
        if not img:
            return url

        x, y = img.size
        if x < 48 and y < 48:
            return None

        if img:
            data = StringIO()
            if not url.endswith('gif'):
                img = pic_fit_width_cut_height_if_large(img, 721)
                img.save(data, 'JPEG')
            else:
                img.save(data, 'gif')
            save_to_md5_file_name(UPYUN_PATH_BUILDER, data.getvalue(), url)
            data.close()

    if not exists(upyun_url):
        upyun_rsspic.upload(file_path)

    return upyun_url


if __name__ == '__main__':
    #print upyun_fetch_pic('http://www.ifanr.com/wp-content/uploads/2012/01/timeline-the-story-of-your-life.jpeg')
    print exists('http://1.42qu.us/4ec22cb3b11734330557f229bfa44aa6.jpg')
    #print checkURL('http://1.42qu.us/648dcf451b52741e6965ac91d224592e.jpg')
    pass

