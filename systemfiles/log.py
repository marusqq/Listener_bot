#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module for logging'''

from datetime import datetime



def log(log_author, log_message):
    '''opens listener.log, outputs log_message, closes listener.log'''

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    log_file = open('listener.log', 'a+')
    log_file.write('[' + str(current_time) + '] ' + log_author + ': ' + log_message + '\n')
    log_file.close()
    
    return