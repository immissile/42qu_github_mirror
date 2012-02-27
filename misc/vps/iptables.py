#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import getopt

network = "10.10.1.0/24"

def usage ():
    print "%s setup" % (sys.argv[0])
    print "%s portmap --outip [IP] --outport [PORT] --inip [VMIP] --inport [VMPORT]" % (sys.argv[0])

def _call_cmd (cmd):
    res = os.system (cmd)
    if res != 0:
         raise Exception ("%s exit with %d" % (cmd, res))


def setup  ():
    _call_cmd ("echo 1 > /proc/sys/net/ipv4/ip_forward")
    _call_cmd ("iptables -t nat -A POSTROUTING -s 10.10.1.0/24 -j SNAT --to-source 119.254.32.167")

def add_portmap (outip, outport, inip, inport):
    assert inip and outip
    assert isinstance (inport, int)
    assert isinstance (outport, int)
    _call_cmd ("iptables -t nat -A PREROUTING -p tcp --dport %d -d %s -j DNAT --to-destination %s:%d" % (outport, outip, inip, inport))



def main() :
    if len (sys.argv) <= 1:
        usage ()
        return 0
    action = sys.argv[1]
    if action == 'setup':
        setup ()
        return 0
    elif action == 'portmap':
        inport = None
        outport = None
        outip = None
        inip = None
        try:
            optlist, args = getopt.gnu_getopt (sys.argv[2:], "", ['outip=', 'outport=', 'inip=', 'inport='])
            for opt, v in optlist:
                if opt == '--inport':
                    inport = int(v)
                elif opt == '--outport':
                    outport = int(v)
                elif opt == '--outip':
                    outip = v
                elif opt == '--inip':
                    inip = v
        except getopt.GetoptError, e:
            print >> sys.stderr, str(e)
            return -1
        if not inport or not outport or not outip:
            raise Exception ("param error")
        add_portmap (outip, outport, inip, inport) 


if "__main__" == __name__:
    main()

