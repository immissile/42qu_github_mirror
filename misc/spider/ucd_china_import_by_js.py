from json import loads

with open("/mnt/zdata/ucd_china.js") as ucd_china:
    for line in ucd_china:
        line = loads(line)
