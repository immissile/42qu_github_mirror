#coding:utf-8
import _env
from config import UPYUN_USERNAME, UPYUN_PWD, UPYUN_SPACENAME,  UPYUN_URL, UPYUN_DIRNAME, UPYUN_PATH_BUILDER
from zkit.pic import pic_fit_width_cut_height_if_large
from cStringIO import StringIO
from zkit.fetch_pic import fetch_pic
from zkit.upyun import UpYun, exists, save_to_md5_file_name, builder_path
import os

upyun_rsspic = UpYun(UPYUN_URL, UPYUN_USERNAME, UPYUN_PWD, UPYUN_SPACENAME)

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

    print upyun_fetch_pic('http://s7.sinaimg.cn/bmiddle/63fd45b8hb812cd486826&69')
