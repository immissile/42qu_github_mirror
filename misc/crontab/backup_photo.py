#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import sys
import base64
import httplib
import os
import subprocess
from config import UPYUN_ACCOUNT, UPYUN_PWD, UPYUN_SPACE_NAME, UPYUN_URL_HEADER, UPYUN_BACK_DIR

headers = {}

def getNewImages():
    #Find images in db...
    cmd = 'find /mnt/zpage/0/ -type f  -daystart -mtime 0'
    event = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    result = event.communicate()[0].split()
    return result

def uploadFile(filename):
    headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:%s' % (UPYUN_ACCOUNT, UPYUN_PWD))
    headers['Mkdir'] = 'true'
    path = '/' + UPYUN_SPACE_NAME + '/' + UPYUN_BACK_DIR + '/' + filename
    connection = httplib.HTTPConnection(UPYUN_URL_HEADER)
    body_content = open(filename).read()
    connection.request('PUT', path, body_content, headers)
    result = connection.getresponse()
    print result.status, result.reason


if __name__ == '__main__':
    for image in getNewImages():
        print image
        uploadFile(image)

