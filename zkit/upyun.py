#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import httplib
import os
from fetch_pic import fetch_pic
from cStringIO import StringIO
from pic import pic_fit_width_cut_height_if_large
from hashlib import md5
import traceback

PATH_BUILDER = 'test/%s'

username = 'wooparadog'
password = 'k1llk1ll'
spaceName = 'rssimg'
urlheader = 'v0.api.upyun.com'  
domain = 'http://1.42qu.us/%s'
dirName = 'imageBackup'
headers={}

def fetch(url,headers):
    if not headers:
        headers = { 
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
                'Accept': ' text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
                'Accept-Language':'zh-cn,zh;q=0.5',
                'Accept-Charset':'gb18030,utf-8;q=0.7,*;q=0.7',
                'Content-type':'application/x-www-form-urlencoded'
                }   

    request = urllib2.Request(
            url,
            headers=headers
            )   
    urlopener = urllib2.build_opener()
    r = urlopener.open(request)

    j = r.read()

    return j

def uploadFile(filename):
    headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))
    headers['Mkdir'] = 'true'
    path = os.path.join('/',spaceName ,os.path.basename(filename))
    connection =  httplib.HTTPConnection(urlheader)
    body_content = open(filename).read()
    connection.request('PUT',path,body_content,headers)
    result = connection.getresponse()
    #print result.status, result.reason

def save_rss_pic(url):

    filename = md5(url).hexdigest()+'.jpg'
    file_path = PATH_BUILDER%filename[:10]
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = os.path.join(file_path,filename)

    if not os.path.exists(file_path):
        print "Downing"
        img = fetch_pic(url)
        if img:
            with open(file_path,'w') as f:
                img = pic_fit_width_cut_height_if_large(img, 721)
                img.save(f,'JPEG')
            uploadFile(file_path)

    return domain%filename
