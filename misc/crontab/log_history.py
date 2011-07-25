#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.log_history import log_num


@single_process
def main():
    log_num()

if __name__ == '__main__':
    main()
