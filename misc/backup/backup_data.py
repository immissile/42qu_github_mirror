#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from os.path import dirname, abspath
import sys

PREFIX = dirname(abspath(__file__))
sys.path = [dirname(dirname(PREFIX))] + sys.path

from config import DB_CONFIG

COMM_OPTION = ' -h%s -P%s -u%s -p%s %s '
def backup_data(host, port, name, user, password):
    comm_option = COMM_OPTION % (host, port, user, password, name)

    """
    备份一个表数据的命令实例
    mysqldump --skip-opt --no-create-info 数据库名字 表名 --where="id<2000"
    """
    create_table_option = ' --no-create-info --quick --default-character-set=utf8 --skip-opt --hex-blob '+comm_option

    cmd = 'mysqldump ' + create_table_option
#    print cmd
    subprocess.Popen(
        cmd.split()
        #stdout=sys.stdout
    )


def backup_main():
    table = DB_CONFIG['main']['master']
    host, port, name, user, password = table.split(':')
    backup_data(host, port, name, user, password)


if __name__ == '__main__':
    backup_main()

"""
create_table_option = comm_option +  "--skip-opt --no-create-info hao123"

cmd = "mysqldump "+create_table_option
print cmd

with open("data.sql", "w") as backfile:
    subprocess.Popen(
        cmd.split(),
        stdout=backfile
    )
"""
