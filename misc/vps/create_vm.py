#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import config
import sys

import re
import os
import subprocess
import getopt
import hashlib
import time
import shutil

from config.vps import BASE_PATH as base_path , NBD_DEVICE as nbd_device


if not os.path.isdir (base_path):
    raise Exception ("%s not exists" % (base_path))


vm_base_dir = os.path.join (base_path, "vm")
baseimg_dir = os.path.join (base_path, "baseimg")
user_script_src = os.path.join (os.path.dirname (__file__), "_create_user.py")
if not os.path.exists (user_script_src):
   raise Exception ("%s not exists" % (user_script_src)) 


def usage ():
    print "usage:\n%s --name [VM_NAME] --baseimg [BASE_IMAGE] --ip [VM_IP/VM_MASK] --gateway [VM_GATEWAY] --user [USER:PASSWD]" % (sys.argv[0])
    os._exit (0)


def _call_cmd (cmd):
    res = os.system (cmd)
    if res != 0:
        raise Exception ("%s exit with %d" % (cmd, res))


def _setup_loop (img_path):
    """ return loop device filename """
    img_path = os.path.abspath (img_path)
    _call_cmd ("losetup -f %s" % (img_path))
    _out = subprocess.check_output (["losetup", "-a"])
    lines = _out.split ("\n")
    for line in lines:
        if line.find (img_path) != -1:
            om = re.match (r"^(/dev/loop\d+):.*$", line)
            if om:
                return om.group (1)

def _teardown_loop (lo_dev):
    _call_cmd ("losetup -d %s" % (lo_dev))


def md5sum_file (path):
    f = open (path, "r")
    try:
        _md5 = hashlib.md5 ()
        while True:
            buf = f.read (10240)
            if buf == "": break
            _md5.update (buf)
    except IOError, e:
        f.close ()
        raise e
    f.close ()
    return _md5.hexdigest ()

def _copy_baseimage (baseimg):
    if not os.path.exists (baseimg_dir):
        os.makedirs (baseimg_dir)
    st = os.stat (baseimg)
    new_baseimg = os.path.join (baseimg_dir, "%s_%s_%s" % (os.path.basename (baseimg), str(st.st_ctime), str(st.st_size)))
    if os.path.isfile (new_baseimg):
        print "%s exists, use it directly" % (new_baseimg)
        return new_baseimg
    else:
        print "copying base image"
        _call_cmd ("cp --sparse=always %s %s" % ( baseimg, new_baseimg))
    return new_baseimg

def _create_inc_image (baseimg, img_path, img_format):
    cmd = "qemu-img-xen create -f %s -b %s %s" % (img_format, baseimg, img_path)
    _call_cmd (cmd)

def _create_raw_image (img_path, mkfs, size):
    """ size in MB, must be an integer """
    cmd = "dd if=/dev/zero of=%s bs=1M count=1 seek=%d" % (img_path, size) # sparse file
    _call_cmd (cmd)
    lo_dev = _setup_loop (img_path)
    time.sleep (1)
    try:
        _call_cmd ("%s %s" % (mkfs, lo_dev))
    finally:
        _teardown_loop (lo_dev)
 

def create_xen_vm (vm_name, baseimg, mem_size=256, disk2_size=10000, disk2_format="ext4", swap_size=512):
    """ mem_size/disk2_size unit in MB, 
        if vm_dir already exists, skip and return None,
        otherwise return (vm_config_path, disk1_path) that we created
    """
    assert isinstance (disk2_size, int)
    assert isinstance (mem_size, int)
    vm_path = os.path.join (vm_base_dir, vm_name)
    if not os.path.exists (vm_path):
        os.makedirs (vm_path)
    config_path = os.path.join (vm_path, "config")
    disk1_path = os.path.join (vm_path, "disk1")
    disk2_path = os.path.join (vm_path, "disk2")
    if os.path.exists (config_path) or os.path.exists (disk1_path):
        print "existing file in %s is blocking the path, skip it" % (vm_path)
        return None
    new_baseimg = _copy_baseimage (baseimg) 
    print "create disk1"
    _create_inc_image (new_baseimg, disk1_path, "qcow") 
    print "create disk2"
    _create_raw_image (disk2_path, "mkfs." + disk2_format, disk2_size)
    swap_path = os.path.join (vm_path, "swap")
    print "create swap"
    _create_raw_image (swap_path, "mkswap", swap_size)

    vm_config_content = """
name = "%s"
maxmem = %d
memory = %d
vcpus = 1
kernel = "/mnt/nova/xen/kernel/kernel-3.2.1-r2-domu"
root = "/dev/xvda1 ro"
extra="xencons=xvc0 console=tty" 
on_poweroff = "destroy"
on_reboot = "restart"
on_crash = "destroy"
sdl = 0
vnc = 0
vncunused = 1
vnclisten = "0.0.0.0"
disk = [ "tap:qcow:%s,xvda1,w", "tap:aio:%s,xvdb1,w", "file:%s,xvdc1,w"]
vif = ["bridge=br0"]
""" % (vm_name, mem_size, mem_size, disk1_path, disk2_path, swap_path)
    f = open (config_path, "w+")
    try:
        f.write (vm_config_content)
    finally:
        f.close ()
    print "vm config and image created"
    return (config_path, disk1_path)

def _mount_img (img_path, tmp_mount):
    if not os.path.exists (tmp_mount):
        os.makedirs (tmp_mount)
    _call_cmd ("qemu-nbd --connect=%s %s" % (nbd_device, img_path))
    time.sleep (3)
    try:
        _call_cmd ("mount %s %s" % (nbd_device, tmp_mount))
    except Exception, e:
        _call_cmd ("qemu-nbd --disconnect %s" % (nbd_device))
        raise e

def _umount_img (tmp_mount):
    _call_cmd ("umount %s" % (tmp_mount))
    _call_cmd ("qemu-nbd --disconnect %s" % (nbd_device))

def do_vm_config (vm_disk1_path, disk2_format, vm_name, vm_ip, vm_netmask, vm_gateway, user_dict):
    tmp_mount = "/tmp/vm_mount"
    _mount_img (vm_disk1_path, tmp_mount)
    print "mounted vm_img"
    print "config hostname"
    vm_net_config_content = """
config_eth0="%s/%d"
routes_eth0="default via %s"
    """ % (vm_ip, vm_netmask, vm_gateway)
    fstab_entry = """
/dev/xvdb1   /data  %s defaults 0 0
/dev/xvdc1    none  swap defaults 0 0
""" % (disk2_format)
    try:
        data_mount_point = os.path.join (tmp_mount, "data")
        if not os.path.exists (data_mount_point):
            os.makedirs (data_mount_point)
        f = open (os.path.join (tmp_mount, "etc/conf.d/hostname"), "w+")
        try:
            f.write ('hostname="%s"\n' % (vm_name))
        finally:
            f.close ()
        f = open (os.path.join (tmp_mount, "etc", "conf.d", "net"), "w+")
        try:
            f.write (vm_net_config_content)
        finally:
            f.close ()
        f = open (os.path.join (tmp_mount, "etc/fstab"), "a")
        try:
            f.write (fstab_entry + "\n")
        finally:
            f.close ()
        user_script_dest = os.path.join (tmp_mount, "tmp", "_create_user.py")
        user_data = os.path.join (tmp_mount, "tmp", "user_data")
        shutil.copy (user_script_src, user_script_dest)
        f = open (user_data, "w")
        try:
            for user, pw in user_dict.iteritems ():
                f.write ("%s:%s\n" % (user, pw))
        finally:
            f.close ()
        if os.system ("chroot %s python /tmp/_create_user.py" % (tmp_mount)):
            print "create user failed"
        os.unlink (user_data)
        os.unlink (user_script_dest)
    finally:
        _umount_img (tmp_mount)


def main ():
    optlist = []
    args = []
    vm_name = None
    vm_ip = None
    vm_netmask = None
    vm_passwd = None
    user_dict = dict ()
    baseimg = None
    ssh_port = None
    if len (sys.argv) == 1:
        usage ()
        return 0
    try:
        optlist, args = getopt.gnu_getopt (sys.argv[1:], "h", ["help", 'baseimg=', 'name=', 'ip=', 'gateway=', 'user='])
    except getopt.GetoptError, e:
        print >> sys.stderr, str(e)
        return -1
    for opt, v in optlist:
        print opt, v
        if opt in ['--help', '-h'] :
            usage ()
            return 0
        elif opt == '--name':
            vm_name = v
        elif opt == '--ip':
            arr = v.split ("/")
            if len(arr) != 2:
                raise Exception ("ip format must be in XXX.XXX.XXX.XXX/number")
            vm_ip = arr[0]
            vm_netmask = int(arr[1])
        elif opt == '--gateway':
            vm_gateway = v
        elif opt == '--user':
            arr = v.split (":")
            if len(arr) != 2:
                raise Exception ("param user should be in 'USER:PASSWD' form")
            user_dict[arr[0]] = arr[1]
        elif opt == '--baseimg':
            baseimg = v

    create_vm (vm_name=vm_name, baseimg=baseimg, mem_size=256, disk2_size=10000, swap_size=512,
        vm_ip=vm_ip, vm_netmask=vm_netmask, vm_gateway=vm_gateway, user_dict=user_dict)
    return 0

def create_vm (vm_name, baseimg, mem_size, disk2_size, swap_size, vm_ip, vm_netmask, vm_gateway, user_dict):
    if not baseimg or not vm_ip or not vm_name:
        raise Exception ("param error")
    if not os.path.isfile (baseimg):
        raise Exception ("%s not exist" % (baseimg))
        
    _call_cmd ("modprobe nbd max_part=8")
    res = create_xen_vm (vm_name=vm_name, baseimg=baseimg, mem_size=mem_size, disk2_size=disk2_size, disk2_format="ext4", swap_size=swap_size, )
    if not res:
        return -1
    vm_config_path, vm_disk1_path = res
    do_vm_config (vm_disk1_path=vm_disk1_path, disk2_format="ext4", vm_name=vm_name, vm_ip=vm_ip, vm_netmask=vm_netmask, vm_gateway=vm_gateway, user_dict=user_dict)

    
if "__main__" == __name__:
    res = main ()
    os._exit (res)

