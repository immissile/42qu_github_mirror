#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import config.dev

if __name__ == '__main__':
    from zkit.reloader.reload_server import auto_reload
    from server_m import run
    auto_reload(run)
