#!/usr/bin/env listener
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''script used for a bot which will be listening for messages'''

#main libraries for fbchat
from fbchat import Client

#for various things
import sys
import os
import pyotp

#import various things from systemfiles
    #logging
import systemfiles.log
    #sending mail
import systemfiles.sendmail
    #hardcoded input
import systemfiles.input
    #for deciding what to do with the message_text
import systemfiles.checktext

#-------------------------------------------------------


print ('Listener Started!!!!')

#if we are using hardcoded data
data_from_file = True

#get the data
data_arr = systemfiles.input.get_data(data_from_file)

#-------------------------------------------------------


#overloading client function onMessage
class ListenerBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if True: #and thread_id == data_arr[11] and thread_type == ThreadType.GROUP:

            #if we don't find anything to do here, return false
            if not systemfiles.checktext.decide(client, message_object.text, thread_id, thread_type, author_id):

                # Sends the data to the inherited onMessage, so that we can still see when a message is received
                super(ListenerBot, self).onMessage(
                    author_id=author_id,
                    message_object=message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    **kwargs
                )
    '''so i don't have to input my fa code myself :)'''
    def on2FACode(self):
        totp = pyotp.TOTP(data_arr[9])
        code = totp.now()
        return code

#-------------------------------------------------------

#connect to fb
try:
    #also write out the totp code so I don't need to look at my google authenticator, don't fixed by overloading a function
    #systemfiles.utility.totp(data_arr[9])
    #create the client instance
    client = ListenerBot(data_arr[1], data_arr[3], max_tries = 2)

    while True:
        #listen and do something
        client.listen()

#-------------------------------------------------------

except KeyboardInterrupt:
    #inform that keyboard interrupt was used
    print('Script stopped by KeyboardInterrupt')

    quit()

except:

    #get the exception that came here
    e = sys.exc_info()[0]
    print ('SCRIPT CRASH.\nException that caused this: ' + str(e))

    #inform me through mail
    systemfiles.sendmail.sendInfo(
        mes = str(e),
        subject = 'SCRIPT CRASH!',
        sender_mail = data_arr[5],
        receiver_mail = data_arr[5],
        passw = data_arr[7]
    )

    quit()
