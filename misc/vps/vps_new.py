#!/usr/bin/env python
# -*- coding: utf-8 -*-



import _env
from model._db import Model
from uuid import uuid4
from model.event import event_joiner_user_id_list
from model.user_mail import mail_by_user_id
from mako.template import Template
from model.zsite_url import url_or_id
from os.path import abspath, dirname, join, normpath, exists
from model.mail import sendmail
import envoy
import socket
import os

host = socket.gethostname()
gid = host[1:]
GID = int(gid.isdigit())
PREFIX = normpath(dirname(abspath(__file__)))
TEMPLATE_VPS_SH_PATH = join(PREFIX, 'vps.template')

class Vps(Model):
    pass


def passwd():
    passwd = uuid4().hex[-8:].replace('l', 'k')
    return passwd

STATE_VPS_TO_OPEN = 10  #等待开通
STATE_VPS_OPENED = 20   #已经开通
STATE_VPS_TO_CLOSE = 30 #等待关闭
STATE_VPS_CLOSED = 40   #已经关闭

USERNAME = 'z%s'

def next_id_by_group(group_id):
    r = Vps.raw_sql('select max(id_in_group) from vps where `group`=%s', group_id)
    r = r.fetchone()[0] or 0
    return 1+r

from mako.template import Template

def vps_new(vps):
    username = USERNAME%vps.id_in_group
    if exists("/home/%s"%username):
        print username, "exist"
        return
    if not vps.passwd:
        vps.passwd = passwd()
    vps.state = STATE_VPS_OPENED
    vps.save()
    user_mail = mail_by_user_id(vps.user_id)
    with open(TEMPLATE_VPS_SH_PATH) as template:
        cmd = Template(template.read()).render(
            username=username,
            passwd=vps.passwd,
            prefix=PREFIX,
            user_mail=user_mail,
            user_url=url_or_id(vps.user_id) ,
        )
        tmp_sh = '%s/tmp_sh.sh'%PREFIX
        with open(tmp_sh, 'w') as tmp:
            tmp.write(cmd)
        sh = 'sudo sh %s'%tmp_sh
        r = envoy.run(sh)
        print r.std_out
        print r.std_err
        os.remove(tmp_sh)
        vps_open_mail(user_mail, vps.group, username, vps.passwd)

def vps_open_mail(mail, group, user, passwd):
    host = 'e%s.42qu.us'%group
    subject = 'VPS已开通 : 帐号 %s 主机 %s'%( user, host)
    txt = Template(u"""

本主机仅供 42qu.com 以及 其开源代码 感兴趣的人 研究学习 , 请不要用于其他用途 

主机 : ${host}
用户 : ${user}
密码 : ${passwd}

开发测试的域名 : ${user}e${group}.tk (请参阅 文档2 配置开发域名)

文档 :

1 . 用xshell登录服务器 http://book.42qu.com/linux/xshell.html

2 . 运行42qu.com开源代码 http://book.42qu.com/42qu/newbie.html


数据库 : 

用户名 zpage, 密码 42qudev 

注意  : zpage 和 zpage_google 的共用的开发数据库 , 请不要乱动 

你可以创建自己的 zpage_随便取名字 数据库玩

管理后台 : http://e1sql.42qu.us/

有任何问题请到这里提问 :

https://groups.google.com/group/42qu-school

""").render(
host=host,
user=user,
passwd=passwd,
group=group
)
    sendmail(subject, txt, mail)
    mail = "zsp042@gmail.com"
    sendmail(subject, txt, mail)

def vps_new_by_user_id(user_id, group=GID):
    if not user_id:
        return
    vps = Vps.get(user_id=user_id)
    if not vps:
        vps = Vps(
            id_in_group=next_id_by_group(group),
            group=group,
            state=STATE_VPS_TO_OPEN,
            user_id=user_id,
            passwd=''
        )
        vps.save()
    vps_new(vps)


import socket
host = socket.gethostname()
def vps_list_by_hostname():
    return list(Vps.where(group=GID))

def vps_open_all():
    from passwd import loadpw
    exist = loadpw()
    for i in vps_list_by_hostname():
        username = USERNAME%i.id_in_group
        if username not in exist:
            vps_new(i)

if __name__ == '__main__':
#    vps_open_all()
#    vps_new_by_user_id(10000000, group=GID)
    
    
    url_list = [  " http://snoop.42qu.com "]
    for url in url_list:
        url = url.strip()
        from model.zsite import zsite_by_query
        vps_new_by_user_id(zsite_by_query(url))

#    vps_open_all()

#def main():
#
#    count = 0
#    user_id_list = event_joiner_user_id_list(10236239)
#    print len(user_id_list)
#    for i in user_id_list:
#
#        count += 1
#
#
#        ip_offset = 19
#        ssh_port_offset = 53000
#        id_in_group = vps.id_in_group
#
#        ip = '10.10.1.%s'%(ip_offset + id_in_group)
#        ssh_port = ssh_port_offset + id_in_group
#
#
##假定虚机名为vmtest, ip 是10.10.1.150 , work的密码是hahaha，要映射ssh到 20352端口的话
##
#
#        vps_new(vps.id, i, ip, ssh_port, vps.passwd)
#
#
#def vps_new(_id, user_id, ip, ssh_port, passwd):
#    username = 'v%s'%_id
#    mail = mail_by_user_id(user_id)
#
##    return
#    if _id != 149:
#        return
#    print 'echo %s:%s| chpasswd'%(username, passwd)
#    print mail
#    print ""
##    subject = "[42qu.培训班] 下节课的预习材料"
##    text = """
##
##上节课的讲义
##http://book.42qu.com/linux/vim.html
##
##下节课的预习
##
##版本控制
##http://book.42qu.com/tool/hg.html
##http://book.42qu.com/tool/git.html
##
##数据库
##http://book.42qu.com/database/index.html
##
##PS: 没有开通主机的同学 请邮件到我邮箱 zsp007@gmail.com 标题为 "[主机.42培训班] + 你的42qu注册帐号"
##
##另外请加入
##Google groups https://groups.google.com/group/42qu-school
##QQ群 : 211707205
##"""
#
#
#    subject = '[42qu.培训班] 学习用的主机帐号'
#    text = """
#主机 : 0002.42qu.us
#用户名 : %s
#密码 : %s
#
#如何登录主机
#http://book.42qu.com/linux/introduction.html
#
#预习材料:
#http://book.42qu.com/python/before_started.html
#
#Google groups https://groups.google.com/group/42qu-school
#QQ群 : 211707205
#    """%(username, passwd)
#
#    mail = "epal@qq.com"
#    #mail = 'zsp007@gmail.com'
#    print subject
#    print text
#    sendmail(
#        subject,
#        text, mail
#    )
#
##    result = []
##    cmd = """python create_vm.py --baseimg /mnt/nova/xen/template/ext4_root.img --name vps%s --ip %s/24 --gateway 10.10.1.1 --user work:%s"""%(
##        _id, ip, passwd
##    )
##    result.append(cmd)
##
##    cmd = """python iptables.py portmap --outip 119.254.32.167 --outport %s --inip %s --inport 22"""%(ssh_port, ip)
##
##    result.append(cmd)
##    cmd = """xm create /mnt/nova/xen/vm/vps%s/config """ % (_id)
##    result.append(cmd)
##
##    print "\n".join(result)
##    print ""
##    def _(from_state, to_state, recall):
##        cursor.execute("select id, id_in_group, `passwd`, `group` from vps where state=%s", from_state)
##        for id,  id_in_group, passwd, group in cursor.fetchall():
##            recall(group, id_in_group)
##            cursor.execute("update state=%s where id=%s", (to_state, id))
##
##    if len (sys.argv) <= 1:
##        print "need param"
##        os._exit (1)
##    action = sys.argv[1]
##    if action == 'open':
##        _(STATE_VPS_TO_OPEN, STATE_VPS_OPENED, vps_open)
##    else:
##        raise Exception ("param error")
###    _(STATE_VPS_TO_CLOSE, STATE_VPS_CLOSED, vps_close)
##
##
##
##
#if '__main__' == __name__:
#    main()
##
