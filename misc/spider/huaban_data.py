import _env
from zkit.pprint import pprint
from json import loads

with open("/mnt/zdata/data/huaban.js") as huaban:
    for line in huaban:
        for pin in loads(line)['board']['pins']:
            pprint(pin)
            raw_input()
