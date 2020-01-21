# -*- coding: UTF-8 -*-

from fbchat import log, Client
from fbchat.models import *

#for nophone auth
import pyotp

#for password security
import getpass


import sys


#-------------------------------------------------------
#0. start the script
print ('Listener Started!!!!')

#get all the spicy details
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

#log example                 
#log.info("{} will be removed from {}".format(author_id, thread_id))
logfile = open('history.log', 'w+')

class ListenerBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if True: #and thread_id == data_arr[11] and thread_type == ThreadType.GROUP:   


            if message_object.text == "!help": #and thread_id == data_arr[11] and thread_type == ThreadType.GROUP:
                
                self.send(Message(text = 'Hi, i am ListBot. '), thread_id = thread_id, thread_type = thread_type)
                #log.info('!help used by: {}'.format(author_id))
                logfile.write('!help used by: {}'.format(author_id))




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

except:
    print ('Script has crashed :(')
    e = sys.exc_info()[0]
    print ('Exception that caused this: ' + str(e))
    sendInfo(str(e), 'SCRIPT CRASH!')
    quit()
