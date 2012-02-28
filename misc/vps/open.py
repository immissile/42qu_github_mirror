#!/usr/bin/env python
# -*- coding: utf-8 -*-



import _env
from model._db import Model
from uuid import uuid4
from model.event import event_joiner_user_id_list
from model.user_mail import mail_by_user_id
from model.mail import sendmail

class Vps(Model):
    pass


def password():
    passwd = uuid4().hex[-8:].replace("l", "k")
    return passwd


#import sys
#import os
#
#cursor = cursor_by_table('vps')
#
PORT_SSH_OFFSET = 50000
#
#
STATE_VPS_TO_OPEN = 10  #等待开通
STATE_VPS_OPENED = 20   #已经开通
STATE_VPS_TO_CLOSE = 30 #等待关闭
STATE_VPS_CLOSED = 40   #已经关闭
#
#
#def vps_open(group, id_in_group, vm_id, passwd):
#    ssh_port = id_in_group + PORT_SSH_OFFSET
#
#def vps_close(group, id_in_group):
#    pass
#
#
#

def next_id_by_group(group_id):
    r = Vps.raw_sql("select max(id_in_group) from vps where `group`=%s", group_id)
    r = r.fetchone()[0] or 0
    return 1+r


def main():

    count = 0
    user_id_list = event_joiner_user_id_list(10236239)
    print len(user_id_list)
    for i in user_id_list:

        count += 1
        vps = Vps.get(user_id=i)

        if not vps:
            group = 1
            passwd = password()
            vps = Vps(
                id_in_group=next_id_by_group(group),
                passwd=passwd,
                group=group,
                state=STATE_VPS_OPENED,
                user_id=i
            )
            vps.save()


        ip_offset = 19
        ssh_port_offset = 53000
        id_in_group = vps.id_in_group

        ip = "10.10.1.%s"%(ip_offset + id_in_group)
        ssh_port = ssh_port_offset + id_in_group


#假定虚机名为vmtest, ip 是10.10.1.150 , work的密码是hahaha，要映射ssh到 20352端口的话
#

        vps_new(vps.id, i, ip, ssh_port, vps.passwd)


def vps_new(_id, user_id, ip, ssh_port, passwd):
    username = "v%s"%_id
    mail = mail_by_user_id(user_id)

    print _id
    if not (_id==173 or (user_id in (10000205, 10027978))):
        return
    print "echo %s:%s| chpasswd"%(username, passwd)


    subject = "[42qu.培训班] 学习用的主机帐号" 
    text = """
主机 : 0002.42qu.us
用户名 : %s
密码 : %s

如何登录主机
http://book.42qu.com/linux/introduction.html

预习材料:
http://book.42qu.com/linux/introduction.html
http://book.42qu.com/python/before_started.html

Google groups https://groups.google.com/group/42qu-school
QQ群 : 211707205
    """%(username, passwd)

    sendmail(
        subject,
        text, mail
    )
    
#    result = []
#    cmd = """python create_vm.py --baseimg /mnt/nova/xen/template/ext4_root.img --name vps%s --ip %s/24 --gateway 10.10.1.1 --user work:%s"""%(
#        _id, ip, passwd
#    )
#    result.append(cmd)
#
#    cmd = """python iptables.py portmap --outip 119.254.32.167 --outport %s --inip %s --inport 22"""%(ssh_port, ip)
#
#    result.append(cmd)
#    cmd = """xm create /mnt/nova/xen/vm/vps%s/config """ % (_id)
#    result.append(cmd)
#
#    print "\n".join(result)
#    print ""
#    def _(from_state, to_state, recall):
#        cursor.execute("select id, id_in_group, `passwd`, `group` from vps where state=%s", from_state)
#        for id,  id_in_group, passwd, group in cursor.fetchall():
#            recall(group, id_in_group)
#            cursor.execute("update state=%s where id=%s", (to_state, id))
#
#    if len (sys.argv) <= 1:
#        print "need param"
#        os._exit (1)
#    action = sys.argv[1]
#    if action == 'open':
#        _(STATE_VPS_TO_OPEN, STATE_VPS_OPENED, vps_open)
#    else:
#        raise Exception ("param error")
##    _(STATE_VPS_TO_CLOSE, STATE_VPS_CLOSED, vps_close)
#
#
#
#
if "__main__" == __name__:
    main()
#
