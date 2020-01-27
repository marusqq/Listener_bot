#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module for using random system utilities'''

import os
import shutil

def delete_dir(subreddit):
    '''deletes specified directory with files that are in it'''

    if os.path.isdir( 'C:/Users/marius.pozniakovas/Desktop/randomPyScripts/Listener_bot/' + subreddit):
        shared_files = os.listdir('C:/Users/marius.pozniakovas/Desktop/randomPyScripts/Listener_bot/' + subreddit)
        if shared_files is not None:
            shutil.rmtree('C:/Users/marius.pozniakovas/Desktop/randomPyScripts/Listener_bot/' + subreddit)
