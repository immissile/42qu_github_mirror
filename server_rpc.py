#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zweb.server_tornado import Run
import config
from rpc._application import application

run = Run(config.RPC_PORT, application)

if __name__ == '__main__':
    run()
