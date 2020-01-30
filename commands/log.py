#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module to get log from listener.log'''

#for Message
from fbchat.models import Message

def get_log(client, t_id, t_type, length):
    '''gets log entries and sends it to thread'''

    log_data = []
    length = int(length)

    for line in reversed(list(open('listener.log'))):
        if length > 0:
            line = line.replace(' ', '-')
            log_data.append(line)
            length = length - 1 

    #so its easier to print
    message = ''
    for log_entry in log_data:
        message = str(message) + str(log_entry) + '\n'

    client.send(
    Message(text=message), 
    thread_id=t_id,
    thread_type=t_type,
    )


    return 