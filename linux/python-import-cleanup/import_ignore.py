#coding:utf-8
IMPORT_IGNORE = set(filter(bool,map(str.strip,"""
config
config.dev

""".strip().split("\n"))))

FILE_IGNORE = set(filter(bool,map(str.strip,"""
server_mq.py

""".strip().split("\n"))))


def import_ignore(filename, name):
    if filename.replace("./","").strip() in FILE_IGNORE:
        return True
    name = name.replace("import ",'').strip()
    if name in IMPORT_IGNORE:
        return True


