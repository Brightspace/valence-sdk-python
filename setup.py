#!/usr/bin/env python3

"""
distutils/setuptools install script.

Form of this file borrowed from Kenneth Reitz' requests package
"""

import os
import re
import sys
from codecs import open

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit

_packages = ['d2lvalence', ]
_package_data = ['LICENSE', ]
_requires = ['future >= 0.15.2', 'requests >= 1.2.0', ]

def _get_val_from_mod(k):
    with open('d2lvalence/__init__.py', 'r') as fd:
        return re.search(r'^__{0}__\s*=\s*[\'"]([^\'"]*)[\'"]'.format(k),
                         fd.read(),
                         re.MULTILINE).group(1)

_author = _get_val_from_mod('author')
_license = _get_val_from_mod('license')
_title = _get_val_from_mod('title')
_version = _get_val_from_mod('version')

with open('README.rst', 'r', 'utf-8') as f:
          _readme = f.read()

setup(
    name = _title,
    version = _version,
    description ='D2LValence client library for Python.',
    long_description = _readme + '\n\n',
    author = _author,
    author_email ='Valence@Desire2Learn.com',
    url = 'http://www.desire2learn.com/r/valencehome',
    packages = _packages,
    package_data = {'': _package_data },
    include_package_data = True,
    install_requires = _requires,
    license = _license,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ),
    )
