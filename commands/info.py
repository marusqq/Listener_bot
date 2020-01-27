#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module which will be used for basic information in chat'''

from fbchat.models import Message, Mention

def help(client, t_id, t_type):
    '''displays my name and shows the command for documentation'''

    client.send(
    Message(text = 'Hi, I am ListenBot.\nMy God and Creator is Marius Pozniakovas. Check !info for documentation (ᵔᴥᵔ)'), 
    thread_id = t_id, 
    thread_type = t_type,
    )

    return

def documentation(client, t_id, t_type):
    '''displays a link for outgoing documentation'''

    client.send(
    Message(text="Documentation here: https://docs.google.com/document/d/1_vJeWceRharUbokmOCzBbbv7PLLXbL48T4QawdtNa9U"),
    thread_id=t_id,
    thread_type=t_type,
    )

    return

def ideas(client, t_id, t_type):
    '''displays a link for ideas sheet'''

    client.send(
    Message(text="Submit ideas here: https://docs.google.com/spreadsheets/d/1HQzbVy1QzeT962f_D4hBmlkM9_AHSKPlWTA9IxH9cfY"),
    thread_id=t_id,
    thread_type=t_type,
    )

    return

