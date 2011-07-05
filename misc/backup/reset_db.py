#!/usr/bin/env python
# -*- coding: utf-8 -*-
import init_env
from config import DB_CONFIG
import sys
import subprocess
import time
from init_db import init_db
from os.path import join, dirname, abspath

COMM_OPTION = ' -h%s -P%s -u%s -p%s '
def reset_database(key, host, port, name, user, password):
    comm_option = COMM_OPTION%(host, port, user, password)
    cmd = 'mysql '+comm_option
    cmd = cmd.split()
    with open('table_%s.sql'%key) as input:
        table = input.read()
    sql = [
        cmd + [
'-e', 'drop database %s;create database %s character set binary;'%(name, name)
        ],
        cmd + [
            name, '-e', table
        ]

    ]
    for i in sql:
        subprocess.Popen(i)
        time.sleep(2)

def reset():
    reset = False
    for key, value in DB_CONFIG.iteritems():
        host, port, name, user, password = value.get('master').split(':')
        sure = 'reset'
        path = join(dirname(abspath(__file__)), 'backup_table.sh')
        print path
        backup = raw_input('\n>>> backup table %s ? entry y or n...\n'%name).strip().lower()
        if backup not in ('y', 'n'):
            return
        if backup == 'y':
            subprocess.Popen(path)
        if raw_input(">>> please type '%s' to reset database:\n"%sure).strip() == sure:
            print '\n\nCtrl+C TO CANCEL RESET',
            for i in range(3, -1, -1):
                print i,
                sys.stdout.flush()
                time.sleep(1)
            reset_database(key, host, port, name, user, password)
            print '\nreset %s'%key
            reset = True
    if reset:
        init_db()

if __name__ == '__main__':
    reset()

#from model._db import cursor_by_table
#from config import MYSQL_MAIN
#cursor = cursor_by_table('*')
#def reset():
#    cursor.execute("drop database %s;"%MYSQL_MAIN)
#    cursor.execute('create database %s character set binary;'%MYSQL_MAIN)
#    cursor.connection.commit()
#    with open("table_main.sql") as sql:
#        cursor.executemany(sql.read(),())
#reset()
##if raw_input(">>> please type 'yes_reset_database' to reset_db:\n").strip() == "yes_reset_database":
#    reset()
