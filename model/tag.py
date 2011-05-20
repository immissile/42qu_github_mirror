#!/usr/bin/env python
#coding:utf-8
from kv_table import KvTable

Tag = KvTable('tag')


if __name__ == "__main__":
    print Tag.id_by_value_new("test2")
