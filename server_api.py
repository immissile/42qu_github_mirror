#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _server import Run
import config
from api._application import application

run = Run(config.API_PORT, application)

if __name__ == '__main__':
    run()
