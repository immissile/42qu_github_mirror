#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _server import Run
from god._application import application
import config

run = Run(config.GOD_PORT, application)


if __name__ == '__main__':
    run()
