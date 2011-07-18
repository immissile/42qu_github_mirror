#coding:utf-8
import re
from fanjian import ftoj

CN_CHAR = re.compile(u"[\u4e00-\u9fa5]")
JP_CHAR = re.compile(u"[\u3040-\u309f\u30a0-\u30ff\u31F0-\u31ff]")

def has_cn(txt):
    txt = txt.decode('utf-8', 'ignore')
    txt = ftoj(txt)
    cn = len(CN_CHAR.findall(txt))
    jp = len(JP_CHAR.findall(txt))
    if cn >= 3 and cn > jp*5:
        return True
