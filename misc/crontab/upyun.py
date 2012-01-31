#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import httplib
import os

username = 'wooparadog'
password = 'k1llk1ll'
spaceName = 'rssimg'
urlheader = 'v0.api.upyun.com'  
dirName = 'imageBackup'
headers={}

def getNewImages():
    #Find images in db...
    for image in ['/home/wooparadog/Pictures/misc/Screenshot at 2011-10-19 20:05:30.png','/home/wooparadog/Pictures/misc/YBqVA.jpg']:
        yield image

def uploadFile(filename):
    headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (username, password))
    headers['Mkdir'] = 'true'
    path = os.path.join('/',spaceName ,os.path.basename(filename))
    connection =  httplib.HTTPConnection(urlheader)
    body_content = open(filename).read()
    connection.request('PUT',path,body_content,headers)
    result = connection.getresponse()
    print result.status, result.reason


if __name__ == '__main__':
    for image in getNewImages():
        uploadFile(image)

