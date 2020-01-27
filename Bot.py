#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''script used for a bot which will be listening for messages'''

#main libraries for fbchat
from fbchat import log, Client
from fbchat.models import Message, Mention

#for nophone auth
import pyotp

#for password security
import getpass

#import commands
import commands.basic_reply
import commands.info
import commands.reddit

#import various things from systemfiles
    #logging
import systemfiles.log
    #sending mail
import systemfiles.sendmail
    #hardcoded input
import systemfiles.input
    #for random utilities
import systemfiles.utility

#for sending mail
import smtplib, ssl

#for various things
import sys

#photos start
from fake_useragent import UserAgent
import argparse
import colorama
import json
import os
import re
import requests
import sys
#photos end

#deleting files
import shutil


#-------------------------------------------------------
#0. start the script
print ('Listener Started!!!!')

#start logger
log_file = systemfiles.log.start_log()

#get all the spicy details

##TODO: module for input
#if we are using hardcoded data
data_from_file = True

data_arr = []
#fill empty array with passwords and other sensitive data
if data_from_file:
    with open('data.bin') as file:
        for line in file:
            line = line.rstrip()
            line = line.lstrip()
            data_arr.append(line)

else:
    data_arr.append('Facebook login:')
    data_arr.append(input('Facebook login ----> '))
    
    data_arr.append('Facebook password:')
    psw = getpass.getpass(prompt = 'Facebook password ---> ', stream = None)
    data_arr.append(psw)
    
    data_arr.append('Gmail bot login:')
    data_arr.append(input('Gmail bot username ----> '))
    
    data_arr.append('Gmail bot password:')
    psw = getpass.getpass(prompt = 'Gmail bot password ---> ', stream = None)
    data_arr.append(psw)

    data_arr.append('TOPT auth key:')
    data_arr.append(input('TOPT auth key ----->'))

    data_arr.append('Group Thread ID:')
    data_arr.append(input('Group Thread ID ----->'))

#-------------------------------------------------------


#overloading client function onMessage
class ListenerBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if True: #and thread_id == data_arr[11] and thread_type == ThreadType.GROUP:   

            author_info = client.fetchUserInfo(author_id)
            

            if "!topreddit" in message_object.text:
                
                if "day" in message_object.text or "month" in message_object.text or "year" in message_object.text or 'all' in message_object.text or 'week' in message_object.text:
                    
                    reddit = []
                    reddit = message_object.text.split()
                    commands.reddit.get_and_send_photos_from_reddit(
                        client, 
                        reddit[1], reddit[2], reddit[3],
                        thread_id, thread_type,
                        author_id
                    )

                    #grab_pic(reddit[1], reddit[2], reddit[3])
                    #send_reddit_photos(reddit[1], author_id, thread_id, thread_type)
                    systemfiles.utility.delete_dir(reddit[1])
                else:
                    self.send(Message(text = 'Usage: ![topreddit] [subreddit] [top] [image_count]'), thread_id = thread_id, thread_type = thread_type)
                
            elif message_object.text == "!help":
                systemfiles.log.log(log_file, 'Me', 'test')
                commands.info.help(client, thread_id, thread_type)

            elif message_object.text == "!info":
                commands.info.documentation(client, thread_id, thread_type)

            elif message_object.text == "!ideas":
                commands.info.ideas(client, thread_id, thread_type)

            elif '2iq' in message_object.text:              
                commands.basic_reply.two_iq(client, thread_id, thread_type)

            elif 'lexus' in message_object.text:
                commands.basic_reply.lexus(client, thread_id, thread_type)

            elif 'fat' in message_object.text or 'storas' in message_object.text:
                commands.basic_reply.fat(client, thread_id, thread_type)

            elif 'lenkas' in message_object.text:
                commands.basic_reply.polish(client, thread_id, thread_type)
            
            elif 'bmw' in message_object.text.lower() and author_id == '100001826192111':
                commands.basic_reply.bmw(client, thread_id, thread_type)
            
            else:
                # Sends the data to the inherited onMessage, so that we can still see when a message is recieved
                super(ListenerBot, self).onMessage(
                    author_id=author_id,
                    message_object=message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    **kwargs
                )

#1. try connecting to facebook
username = data_arr[1]
password = data_arr[3]

#2. also get code from totp
totp = pyotp.TOTP(data_arr[9])
code = totp.now()
print('2FA code ----> ' + str(code))


#connect to fb
try:
    client = ListenerBot(username, password, max_tries = 2)
    while True:
        #listen and do something
        client.listen()


except KeyboardInterrupt:
    print('Script stopped by KeyboardInterrupt')
    systemfiles.log.finish_log(log_file)
    quit()

except:
    print ('SCRIPT CRASH')
    e = sys.exc_info()[0]
    print ('Exception that caused this: ' + str(e))

    systemfiles.sendmail.sendInfo(
        mes = str(e), 
        subject = 'SCRIPT CRASH!', 
        sender_mail = data_arr[5], 
        receiver_mail = data_arr[5], 
        passw = data_arr[7]
    )

    systemfiles.log.finish_log(log_file)

    quit()
