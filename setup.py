# -*- coding: utf-8 -*-
"""
    Setup packahe
    ~~~~~~~~~~~~~~~~~~~~

    Setuptools/distutils commands to package installation.

    :author: Marco Lovato/Eng. Streaming
    :contact: maglovato@gmail.com
    :license: Other, see LICENSE for details.
"""
#pylint: HOOK-IGNORED

import os
from setuptools import setup, find_packages

# Hack to silence atexit traceback in newer python versions
try:
    import multiprocessing
except ImportError:
    pass


def get_version(version_tuple):
    if not isinstance(version_tuple[-1], int):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))


init = os.path.join(os.path.dirname(__file__), 'packagesample', '__init__.py')
version_line = list(filter(lambda l: l.startswith('VERSION'), open(init)))[0]
VERSION = get_version(eval(version_line.split('=')[-1]))


def get_requirements(file_name='requirements.txt'):
    filename = open(file_name)
    lines = [i.strip() for i in filename.readlines()]
    filename.close()
    return lines


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        pass
    return ''


CLASSIFIERS = [
    'Environment :: Library',
    'Intended Audience :: End User',
    'Programming Language :: Python',
    'Operating System :: OS Independent',
]

setup(
    author='Marco Lovato',
    author_email='maglovato@gmail.com',
    classifiers=CLASSIFIERS,
    description='Tool for helping organize video and photos',
    entry_points={
        'console_scripts': [
            'packagesample = packagesample.packagesample:main'
        ]
    },
    include_package_data=True,
    install_requires=get_requirements(),
    license=read('LICENSE'),
    long_description=read('README.rst'),
    name='packagesample',
    packages=find_packages(exclude=('tests')),
    platforms=['any'],
    scripts=[],
    test_suite='nose.collector',
    tests_require=get_requirements('requirements-dev.txt'),
    url='http://dsv-str-tools.tpn.terra.com:8000/packages/packagesample',
    version=VERSION,
    zip_safe=True
)
