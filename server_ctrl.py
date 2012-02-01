#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
from zweb.server_tornado_wsgi import Run
from ctrl._zpage import application

run = Run(config.PORT, application)

if __name__ == "__main__":
    run()


