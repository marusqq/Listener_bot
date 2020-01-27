#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''package which will be used for basic replies in chat'''

from fbchat.models import Message, Mention

def two_iq(client, t_id, t_type):
    '''sends "Did you mean Lukas" and tags him'''

    client.send(
    Message(text="Did you mean @Lukas Miezys? Opaaaaaaaaaaaaaaaaaaaaa", 
    mentions=[Mention('100000491391008', offset=13, length=13)]),
    thread_id=t_id,
    thread_type=t_type,
    )

    return

def lexus(client, t_id, t_type):
    '''sends "Guys who buy Lexus..." + stupid clapping wojak'''
    
    client.sendLocalImage(
    "photos/clapping_wojak.png",
    Message(text="Guys who buy Lexus cars in their 20's be like:"),
    thread_id=t_id,
    thread_type=t_type,
    )

    return

def fat(client, t_id, t_type):
    '''sends "mmmm" + fat wojak'''

    client.sendLocalImage(
    "photos/fat_wojak.png",
    Message(text="mmmmmmmmmmmmmmmm"),
    thread_id=t_id,
    thread_type=t_type,
    )

    return

def polish(client, t_id, t_type):
    '''sends "Did you mean Rafal... + tags him + some polska words'''

    client.send(
    Message(text="Did you mean @Rafal Michalkiewicz? Kurwa polski lewandowski", mentions=[Mention('100000494913408', offset=13, length=20)]),
    thread_id=t_id,
    thread_type=t_type,
    )

    return

def bmw(client, t_id, t_type):
    '''sends Want to see Tomas... + wojak with bmw car'''
    client.sendLocalImage(
    "photos/tomas_wojak_bmw.png",
    Message(text="Want to see @Tomas Kučejevas in his 40s with his car????", mentions=[Mention('100001826192111', offset=12, length=16)]),
    thread_id=t_id,
    thread_type=t_type,
    )

    return

