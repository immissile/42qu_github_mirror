#coding:utf-8
IMPORT_IGNORE = set(filter(bool,map(str.strip,"""
config
config.dev

""".strip().split("\n"))))

def import_ignore(name):
    name = name.replace("import ",'').strip()
    if name in IMPORT_IGNORE:
        return True


