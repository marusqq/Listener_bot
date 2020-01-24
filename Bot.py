#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''script used for a bot which will be listening for messages'''

#main libraries
from fbchat import log, Client
from fbchat.models import *

#for nophone auth
import pyotp

#for password security
import getpass

#for sending mail
import smtplib, ssl

#for various things
import sys


#photos
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

def sendInfo(mes, subject = None):
    '''this is used for sending a message to mail'''

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = data_arr[5]  # Enter your address
    receiver_email = data_arr[5]  # Enter receiver address
    password = data_arr[7]



    message = """\
Subject: """ + subject + """
    \n""" + mes

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)



def delete_dir(subreddit):
    if os.path.isdir( 'C:/Users/marius.pozniakovas/Desktop/randomPyScripts/Listener_bot/' + subreddit):
        shared_files = os.listdir('C:/Users/marius.pozniakovas/Desktop/randomPyScripts/Listener_bot/' + subreddit)
        if shared_files is not None:
            shutil.rmtree('C:/Users/marius.pozniakovas/Desktop/randomPyScripts/Listener_bot/' + subreddit)


#log example                 
#log.info("{} will be removed from {}".format(author_id, thread_id))S
logfile = open('history.log', 'w+')


def send_reddit_photos(subreddit, author_id, threadid, threadtype):
    
    code_dir = 'C:/Users/marius.pozniakovas/Desktop/randomPyScripts/Listener_bot/' + 'reddit/' 
    reddit_photos_dir = code_dir + subreddit
    reddit_photos = os.listdir(reddit_photos_dir)
    
    for photo in reddit_photos:
        
        client.sendLocalImage(
                    reddit_photos_dir + '/' + photo,
                    Message(text='Author: this_guy, photo from: ' + subreddit, mentions=[Mention(author_id, offset=8, length=8)]),
                    thread_id=threadid,
                    thread_type=threadtype,
                )
        
#photos
def get_valid_filename(s):
    ''' strips out special characters and replaces spaces with underscores, len 200 to avoid file_name_too_long error '''
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'[^\w.]', '', s)[:200]


def erase_previous_line():
    # cursor up one line
    sys.stdout.write("\033[F")
    # clear to the end of the line
    sys.stdout.write("\033[K")


def get_pictures_from_subreddit(data, subreddit, location):
    for i in range(len(data)):
        current_post = data[i]['data']
        image_url = current_post['url']
        if '.png' in image_url:
            extension = '.png'
        elif '.jpg' in image_url or '.jpeg' in image_url:
            extension = '.jpeg'
        elif 'imgur' in image_url:
            image_url += '.jpeg'
            extension = '.jpeg'
        else:
            continue

        erase_previous_line()
        print('downloading pictures from r/' + subreddit +
              '.. ' + str((i*100)//len(data)) + '%')

        # redirects = False prevents thumbnails denoting removed images from getting in
        image = requests.get(image_url, allow_redirects=False)
        if(image.status_code == 200):
            try:
                output_filehandle = open(
                    location + '/' + get_valid_filename(current_post['title']) + extension, mode='bx')
                output_filehandle.write(image.content)
            except:
                pass


def grab_pic(subreddit, top, image_count):
    colorama.init()
    ua = UserAgent(fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')

    #for j in range(3):
    print('Connecting to r/' + subreddit)
    url = 'https://www.reddit.com/r/' + subreddit + '/top/.json?sort=top&t=' + \
        top + '&limit=' + image_count
    response = requests.get(url, headers={'User-agent': ua.random})
    
    if os.path.exists('C:/Users/marius.pozniakovas/Desktop/randomPyScripts/Listener_bot/reddit/'):
        location = os.path.join('C:/Users/marius.pozniakovas/Desktop/randomPyScripts/Listener_bot/reddit/', subreddit)

    else:
        print('Given path does not exist, try without the location parameter to default to the current directory')
        exit()

    if not response.ok:
        print("Error check the name of the subreddit", response.status_code)
        exit()

    if not os.path.exists(location):
        os.mkdir(location)
    # notify connected and downloading pictures from subreddit
    erase_previous_line()
    print('downloading pictures from r/' + subreddit + '..')

    data = response.json()['data']['children']
    get_pictures_from_subreddit(data, subreddit, location)
    erase_previous_line()
    print('Downloaded pictures from r/' + subreddit)
#photos

class ListenerBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if True: #and thread_id == data_arr[11] and thread_type == ThreadType.GROUP:   

            #author_info = client.fetchUserInfo(author_id)

            #print ('Name: {}'.format(author_info.name))
            #print ('Message: {}'.format(message_object))

            #print(author_info.name)
            if message_object.text == "!help":
                
                self.send(Message(text = 'Hi, I am ListenBot.\nMy God and Creator is Marius Pozniakovas. Check !info for documentation (ᵔᴥᵔ)'), thread_id = thread_id, thread_type = thread_type)
                log.info('!help used by: {}'.format(author_id))
                logfile.write('!help used by: {}'.format(author_id))


            if "!topreddit" in message_object.text:
                
                if "day" in message_object.text or "month" in message_object.text or "year" in message_object.text or 'all' in message_object.text or 'week' in message_object.text:
                    reddit = []
                    reddit = message_object.text.split()
                    grab_pic(reddit[1], reddit[2], reddit[3])
                    send_reddit_photos(reddit[1], author_id, thread_id, thread_type)
                    delete_dir(reddit[1])
                else:
                    self.send(Message(text = 'Usage: ![topreddit] [subreddit] [top] [image_count]'), thread_id = thread_id, thread_type = thread_type)
                



            elif '2iq' in message_object.text:
                self.send(
                    Message(text="Did you mean @Lukas Miezys? Opaaaaaaaaaaaaaaaaaaaaa", mentions=[Mention('100000491391008', offset=13, length=13)]),
                    thread_id=thread_id,
                    thread_type=thread_type,
                )

            elif 'lexus' in message_object.text:
                self.sendLocalImage(
                    "photos/clapping_wojak.png",
                    Message(text="Guys who buy Lexus cars in their 20's be like:"),
                    thread_id=thread_id,
                    thread_type=thread_type,
                )

            elif 'fat' in message_object.text or 'storas' in message_object.text:
                self.sendLocalImage(
                    "photos/fat_wojak.png",
                    Message(text="mmmmmmmmmmmmmmmm"),
                    thread_id=thread_id,
                    thread_type=thread_type,
                )

            elif 'lenkas' in message_object.text:
                self.send(
                    Message(text="Did you mean @Rafal Michalkiewicz? Kurwa polski lewandowski", mentions=[Mention('100000494913408', offset=13, length=20)]),
                    thread_id=thread_id,
                    thread_type=thread_type,
                )

            
            elif 'bmw' in message_object.text.lower() and author_id == '100001826192111':
                self.sendLocalImage(
                    "photos/tomas_wojak_bmw.png",
                    Message(text="Want to see @Tomas Kučejevas in his 40s with his car????", mentions=[Mention('100001826192111', offset=12, length=16)]),
                    thread_id=thread_id,
                    thread_type=thread_type,
                )
            
            elif message_object.text == "!info":
                
                self.send(
                    Message(text="Documentation here: https://docs.google.com/document/d/1_vJeWceRharUbokmOCzBbbv7PLLXbL48T4QawdtNa9U"),
                    thread_id=thread_id,
                    thread_type=thread_type,
                )

            elif message_object.text == "!ideas":
                
                self.send(
                    Message(text="Submit ideas here: https://docs.google.com/spreadsheets/d/1HQzbVy1QzeT962f_D4hBmlkM9_AHSKPlWTA9IxH9cfY"),
                    thread_id=thread_id,
                    thread_type=thread_type,
                )
            
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
