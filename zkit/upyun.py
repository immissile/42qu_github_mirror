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
from config import UPYUN_USERNAME,UPYUN_PWD,UPYUN_SPACENAME,UPYUN_API_URL,UPYUN_DOMAIN,UPYUN_DIRNAME,UPYUN_PATH_BUILDER

class UpYun(object):
    def __init__(self, domain,username,password,spacename, headers={}):
        self.domain,self.username,self.password,self.headers,self.spacename = domain,username,password,headers,spacename
        self.headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (self.username, self.password))
        self.headers['Mkdir'] = 'true'

    def append(self,  url, path_builder=UPYUN_PATH_BUILDER):
        filename = md5(url).hexdigest()+'.jpg'
        file_path = path_builder%filename[:10]
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_path = os.path.join(file_path, filename)

        if not os.path.exists(file_path):
            img = fetch_pic(url)
            if img:
                with open(file_path, 'w') as f:
                    img = pic_fit_width_cut_height_if_large(img, 721)
                    img.save(f, 'JPEG')
                self.upload(file_path)
        return self.domain%filename


    def upload(self,filename):
        path = os.path.join('/', self.spacename , os.path.basename(filename))
        connection = httplib.HTTPConnection(UPYUN_API_URL)
        body_content = open(filename).read()
        connection.request('PUT', path, body_content, self.headers)
        result = connection.getresponse()
        

upyun_rsspic = UpYun(UPYUN_DOMAIN,UPYUN_USERNAME,UPYUN_PWD,UPYUN_SPACENAME)

def upyun_fetch_pic(url):
    return upyun_rsspic.append(url)
