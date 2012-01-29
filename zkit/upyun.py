#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import base64
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

    #def append(self,  url, path_builder=UPYUN_PATH_BUILDER):
    #    filename = md5(url).hexdigest()+'.jpg'
    #    #file_path = path_builder%filename[:10]
    #    file_path = path_builder%( "/".join([filename[:2], filename[2:4]]))
    #    if not os.path.exists(file_path):
    #        os.makedirs(file_path)
    #    file_path = os.path.join(file_path, filename)
    #    if not os.path.exists(file_path):
    #        img = fetch_pic(url)
    #        if img:
    #            with open(file_path, 'w') as f:
    #                img = pic_fit_width_cut_height_if_large(img, 721)
    #                img.save(f, 'JPEG')
    #            self.upload(file_path)
    #    return self.domain%filename

    def upload(self, filename):
        with open(filename) as f:
            data = f.read()
            self.upload_data(filename, data)

    def upload_data(self, path, data):
        path = os.path.join('/', self.spacename , os.path.basename(path))
        connection = httplib.HTTPConnection(UPYUN_API_URL)
        connection.request('PUT', path, data, self.headers)
        result = connection.getresponse()
        print result.status, result.reason,self.domain%os.path.basename(path)
        return self.domain%os.path.basename(path)

    def upload_img(self, path, img):
        data = StringIO()
        img.save(data,'JPEG')
        url = self.upload_data(path,data.getvalue())
        data.close()
        return url

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


upyun_rsspic = UpYun(UPYUN_DOMAIN, UPYUN_USERNAME, UPYUN_PWD, UPYUN_SPACENAME)

def upyun_fetch_pic(url):
    file_path, filename = builder_path(UPYUN_PATH_BUILDER, url)
    if not os.path.exists(file_path):
        img = fetch_pic(url)
        data = StringIO()
        if not url.endswith('gif'):
            img = pic_fit_width_cut_height_if_large(img, 721)
            img.save(data, 'JPEG')
        else:
            img.save(data, 'gif')
        save_to_md5_file_name(UPYUN_PATH_BUILDER, data.getvalue(), url)
        data.close()

        upyun_rsspic.upload(file_path)
    return upyun_rsspic.domain%filename

if __name__ == '__main__':
    print upyun_fetch_pic('https://www.upyun.com/images/logo.gif')
