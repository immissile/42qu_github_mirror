#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension(
        'zrank_sort',
        ['zrank_sort.pyx']
    )
]

setup(
    name='zrank',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    author_email='underdarkeye@gmail.com',
    require=['pyrex'],
    version='0.001',
    description='zrank',
)
