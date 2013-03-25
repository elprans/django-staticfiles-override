#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-staticfiles-override',
    version='1.0.0',
    description='Django staticfiles override module.',
    author='Elvis Pranskevichus',
    author_email='elprans@sprymix.com',
    long_description=open('README.rst', 'r').read(),
    url='https://github.com/elprans/django-staticfiles-override',
    packages=[
        'staticfiles_override',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
