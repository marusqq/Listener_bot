#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module for using random system utilities'''

#for delete_dir
import os
import shutil

#for totp
import pyotp

def delete_dir(directory):
    '''deletes specified directory with files that are in it'''

    if os.path.isdir(directory):
        shared_files = os.listdir(directory)
        if shared_files is not None:
            shutil.rmtree(directory)

    return 

def totp(code):

    totp = pyotp.TOTP(code)
    code = totp.now()
    print('TOTP code ----> ' + str(code))

    return code