#coding:utf-8
import re
def txt_wrap_by(begin, end, html):
    if not html:
        return ""
    start = html.find(begin)
    if start >= 0:
        start += len(begin)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def txt_wrap_by_all(begin, end, html):
    if not html:
        return ""
    result = []
    from_pos = 0
    while True:
        start = html.find(begin, from_pos)
        if start >= 0:
            start += len(begin)
            endpos = html.find(end, start)
            if endpos >= 0:
                result.append(html[start:endpos].strip())
                from_pos = endpos+len(end)
                continue
        break
    return result

def strip_line(txt):
    if not txt:
        return ""
    txt = txt.replace("　", " ").split("\n")
    return "\n".join(i for i in [i.strip() for i in txt] if i)

def strip_txt_wrap_by(begin, end, html):
    if not html:
        return ""
    t = txt_wrap_by(begin, end, html)
    if t:
        return strip_line(t)


