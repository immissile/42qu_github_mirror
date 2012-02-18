#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


with open("freq/w2.txt") as freq:
    for line in freq:
        line = line.strip()
        topic , freq , word = line.split(" ",2)
        topic = int(topic)
        freq = int(freq)
        print topic, freq, word

def main():
    pass


if "__main__" == __name__:
    main()

