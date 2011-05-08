#!/usr/bin/env python
#coding:utf-8

MYSQLPORT = 3306
MYSQLPASSWD = "zpagepasswd"
MYSQLUSER = "zpage"

DB_HOST_MAIN = "127.0.0.1:%s:zpage_main:%s:%s"%(MYSQLPORT, MYSQLUSER, MYSQLPASSWD)

DB_CONFIG = {
    "main":{
        "master": DB_HOST_MAIN,
        "tables": (
            '*'
        )
    }
}
