#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module for logging'''

def start_log():
    log_file = open('listener.log', 'w+')
    return log_file

def log(log_file, log_message, log_author):
    log_file.write(log_author + ': ' + log_message)
    return

def finish_log(log_file):
    log_file.close()
    return