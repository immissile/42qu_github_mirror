#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base64 import urlsafe_b64encode
from hashlib import md5
from os import walk
from os.path import dirname, join, abspath, basename, exists
from shutil  import copyfile
from struct import pack
from zlib import crc32
import re
import subprocess

prefix = dirname(abspath(__file__))
merge_prefix = prefix
import sys
sys.path.append(dirname(prefix))
from config import FS_URL

def walk_filter(basedir, dirfilter=None, filefilter=None):
    for dirpath, dirnames, filenames in walk(basedir):
        if dirfilter and not dirfilter(dirpath):
            continue
        prefix = dirpath[len(basedir)+1:]
        for filename in filenames:
            if filefilter and not filefilter(filename):
                continue
            yield join(prefix, filename)

class ChangeFilter():
    def __init__(self, buffer_file):
        self.filename2num = dict()
        self.filename2hash = dict()
        self.buffer_file = buffer_file
        self.salt = ''

    def __call__(self, basedir, filelist):
        filelist = list(filelist)
        buffer_file = self.buffer_file
        if exists(buffer_file):
            init_py = open(buffer_file)
            hash_lines = [
                i.strip() for i in
                list(init_py)
            ]
            hash_lines = [
                i for i in hash_lines if i
            ]
            init_py.close()
        else:
            hash_lines = []

        if hash_lines:
            self.salt = hash_lines[0]
            hash_lines = hash_lines[1:]
        else:

            from os import urandom
            self.salt = urlsafe_b64encode(urandom(3))[:3]


        for i in hash_lines:
            hash, num, filename = i.split()
            self.filename2hash[filename] = hash
            self.filename2num[filename] = int(num)

        has_change = False
        for i in filelist:
            fpath = join(basedir, i)
            with open(fpath) as inf:
                txt = inf.read()
                hash = md5(txt).hexdigest()
                result = self.filename2hash.get(i)
                if result == hash:
                    continue
                if result is None:
                    self.filename2num[i] = 1
                else:
                    self.filename2num[i] += 1
                    has_change = True
                print fpath
                self.filename2hash[i] = hash
                #    print i,hash,result,self.filename2hash
                yield i

        if has_change:
            for k in ('z.css'):
                if k in self.filename2num:
                    self.filename2num[k] += 1

        existed_key = set(filelist)
        #print existed_key
        self.filename2hash = dict([
            (k, v) for k, v in self.filename2hash.iteritems() if k in existed_key
        ])


    def flush(self):
        with open(self.buffer_file, 'w') as inf:
            inf.write('%s\n'%self.salt)
            #print self.filename2hash
            for filename, hash in self.filename2hash.iteritems():
                inf.write(
                    '%s\t%s\t%s\n'%(hash, self.filename2num[filename], filename)
                )

def merge(subdir, template):
    file_hash_version = ChangeFilter(
        join(prefix, '.%s_hash'%subdir)
    )
    subdir = join(prefix, subdir)
    for i in file_hash_version(
        subdir,
        walk_filter(subdir, lambda x:x.find('.svn')==-1, lambda x:(x.endswith('.css') or x.endswith('.js')) and not x.startswith('.'))
    ):
        infile = join(subdir, i)
        bi = basename(i)
        outfile = join(subdir, i[:-len(bi)]+'.'+bi)
        if infile.endswith('.js'):
            filetype = 'js'
            cmd = [
                    'uglifyjs', '-o', outfile, infile ,
            ]
        else:
            filetype = 'css'
            cmd = [
                    'java', '-jar', join(prefix, 'yuicompressor.jar'), '--charset=utf-8', '--type', filetype, infile, '-o', outfile
            ]
        try:
            returncode = subprocess.call(cmd)
            if returncode:
                raise
        except Exception, e:
            file_hash_version.filename2num[i] -= 1
            file_hash_version.filename2hash[i] = '0'
            print 'compressor error : %s , %s'%(infile, e)
            copyfile(infile, outfile)
        s = ''
        with open(outfile, 'r') as input:
            s = input.read()
            s = s.replace(';}', '}')
        with open(outfile, 'w') as output:
            output.write(s)

    file_hash_version.flush()
    from mako.template import Template
    init_template = Template(template)
    init_py_file = join(subdir, '__init_file_hash__.py')
    with open(init_py_file, 'w') as init_py:
        filenum = file_hash_version.filename2num.iteritems()
        init_py.write(
            '#coding:utf-8\n\n'+init_template.render(
                filename2num=dict(
                    (
                        k,
                         '%s%s'%(
                            file_hash_version.salt,
                            urlsafe_b64encode(
                                pack('Q', v).rstrip('\x00')
                            ).rstrip('=')
                        )
                    )
                    for k, v in
                    file_hash_version.filename2num.iteritems()
                )
            )
        )

JS_INIT_TEMPLATE = '''\
<%!
from os.path import join,basename,dirname
%>
from config import DEBUG
from config import FS_URL

if DEBUG:
    ORG_CSS_JS = True
else:
    ORG_CSS_JS = False


if ORG_CSS_JS:
%for path,num in filename2num.iteritems():
<%
path = path.rsplit('.js', 1)[0]
name = path.replace('/', '_').replace('.', '_').replace('-', '_')
%>
    ${name} = '%s/js/${path}.js' % FS_URL
%endfor

else:
%for path,num in filename2num.iteritems():
<%
path = path.rsplit('.js',1)[0]
name = path.replace('/', '_').replace('.', '_').replace('-', '_')
pathdir = join('js', dirname(path))
pathfile = basename(path)
filename = join(pathdir, '~%s~%s.js' % (num, pathfile)).replace('\\\\', '/')
%>
    ${name} = '%s/${filename}' % FS_URL
%endfor
'''

#swf = 'http://ajax.googleapis.com/ajax/libs/swfobject/2.2/swfobject.js'
jquery = 'http://lib.sinaapp.com/js/jquery/1.6.2/jquery.min.js'
jquery_ui_prefix = 'http://lib.sinaapp.com/js/jquery-ui/1.8.11'
jquery_ui = '%s/jquery-ui.min.js'%jquery_ui_prefix
#jquery_ui_date_cn = '%s/i18n/jquery.ui.datepicker-zh-CN.js'%jquery_ui_prefix
#
#
#JS_INIT_TEMPLATE += '''
#jquery = '%s'
#jquery_ui = '%s'
#jquery_ui_date_cn = '%s'
#swf = '%s'
#''' % (
#    jquery,
#    jquery_ui,
#    jquery_ui_date_cn,
#    swf
#)

CSS_INIT_TEMPLATE = '''\
<%!
from os.path import join,basename,dirname
%>
from config import DEBUG
from config import FS_URL

if DEBUG:
    ORG_CSS_JS = True
else:
    ORG_CSS_JS = False


if ORG_CSS_JS:
%for path,num in filename2num.iteritems():
<%
path = path.rsplit('.css', 1)[0]
name = path.replace('/', '_').replace('.', '_').replace('-', '_')
%>
    ${name}_ = "%s/css/${path}.css"%FS_URL
    ${name} = '<link href="%s" rel="stylesheet" type="text/css">' % ${name}_
%endfor

else:
%for path,num in filename2num.iteritems():
<%
path = path.rsplit('.css', 1)[0]
name = path.replace('/', '_').replace('.', '_').replace('-', '_')
pathdir = join('css', dirname(path))
pathfile = basename(path)
filename = join(pathdir, '~%s~%s.css' % (num,pathfile)).replace('\\\\','/')
%>
    ${name}_ = "%s/${filename}"%FS_URL
    ${name} = '<link href="%s" rel="stylesheet" type="text/css">'%${name}_
%endfor
'''


def merge_css_import(path):
    pathdir = dirname(path)
    filename = basename(path)
    txt = ''
    with open(path) as f:
        txt = f.read()
    def sub(match):
        t = n = match.groups()[0]
        t = t[t.find('(')+1:t.find(')')]
        if '://' in t:
            return n
        path = join(pathdir, dirname(t), '.'+basename(t))
        if exists(path):
            with open(path) as r:
                return r.read()
    new = re.sub('(@import\s+?url\([^)]+?\)\s*;)', sub, txt)
    if txt != new:
        with open(join(pathdir, '.'+filename), 'w') as g:
            g.write(new)

def merge_js(path, filename, filetuple):
    filepath = join(path, filename)
    txt = [';'] #不加开头的;uglifyjs 不压缩开头的注释


    for i in filetuple:
        with open(join(path, i), 'r') as infile:
            txt.append(infile.read())
    with open(filepath, 'w') as out:
        out.write('\n;\n'.join(txt))


def merge_js_import(path, filename, filetuple):
    filepath = join(path, filename)
    txt = ['''
function LOAD(js){
    document.write('<script src="'+js+'"></'+"script>")
}
''']

    for i in filetuple:
        txt.append("LOAD('%s/js/%s')"%(FS_URL, i))

    with open(filepath, 'w') as out:
        out.write('\n'.join(txt))


import js_z
merge('css', CSS_INIT_TEMPLATE)
print 'CSS Merge Game Over'

merge_js(join(prefix, 'js'), 'z.js', js_z.JS)

merge('js', JS_INIT_TEMPLATE)
print 'JS Merge Game Over'

merge_css_import(join(prefix, 'css', 'z.css'))
merge_js_import(join(prefix, 'js'), 'z.js', js_z.JS)
