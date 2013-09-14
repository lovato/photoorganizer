# -*- coding: UTF-8 -*-
'''
Created on 07/03/2013

@author: marco.lovato
'''
VERSION = (0, 0, 1)

def get_version(version_tuple=VERSION):
    if not isinstance(version_tuple[-1], int):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))