#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module for using reddit download pictures command'''

#The guy who wrote the core as I only customised it:
#   https://github.com/nobodyme/reddit-fetch
#   by @nobodyme

#libs used
from fake_useragent import UserAgent
import argparse
import colorama
import json
import os
import re
import requests
import sys

#use utility for getting name
import systemfiles.utility

#this is needed for message and mention parameters
from fbchat.models import Message, Mention

#main function to split the workflow
def get_and_send_photos_from_reddit(client, subreddit, top, images, t_id, t_type, author_id):
    '''main function which will split the workflow'''

    grab_pic(subreddit, top, images)
    send_reddit_photos(client, subreddit, author_id, t_id, t_type)

    return

def send_reddit_photos(client, subreddit, author_id, threadid, threadtype):
    '''sends photos from directory to facebook's thread, tags the author and also specifies what subreddit is used'''

    code_dir = os.getcwd() + '/downloaded_photos/reddit/'
    reddit_photos_dir = code_dir + subreddit
    reddit_photos = os.listdir(reddit_photos_dir)

    #if we have atleast one photo
    if len(reddit_photos) > 0:

        author_name = systemfiles.utility.get_name(client, author_id)

        #first what we did
        client.send(
            Message(text='Photos asked by: ' + author_name + ', ' + str(len(reddit_photos)) + ' photos from [r/' + subreddit + '] below:',
            mentions=[Mention(author_id, offset=17, length=len(author_name))]),
            thread_id=threadid,
            thread_type=threadtype,
        )

        #send all photos
        for photo in reddit_photos:

            client.sendLocalImage(
                reddit_photos_dir + '/' + photo,
                thread_id=threadid,
                thread_type=threadtype,
                )

        return

    #if we have less than 1 photo
    else:
        #no photos was used
        client.send(
            Message(text='No photos downloaded from [r/' + subreddit + ']'),
            thread_id=threadid,
            thread_type=threadtype,
        )

        return


def get_valid_filename(s):
    ''' strips out special characters and replaces spaces with underscores, len 200 to avoid file_name_too_long error '''
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'[^\w.]', '', s)[:200]

def erase_previous_line():
    '''erases the previous line'''
    # cursor up one line
    sys.stdout.write("\033[F")
    # clear to the end of the line
    sys.stdout.write("\033[K")

def get_pictures_from_subreddit(data, subreddit, location):
    '''the function that gets the images'''
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
        print('Downloading pictures from r/' + subreddit +
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
    '''grabs the image from subreddit, sorted by top and counter by image_count'''
    colorama.init()
    ua = UserAgent(fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')

    print('Connecting to r/' + subreddit)
    url = 'https://www.reddit.com/r/' + subreddit + '/top/.json?sort=top&t=' + \
        top + '&limit=' + image_count
    response = requests.get(url, headers={'User-agent': ua.random})

    if os.path.exists(os.getcwd() + '/downloaded_photos/reddit/'):
        location = os.path.join(os.getcwd() + '/downloaded_photos/reddit/', subreddit)

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

    print('Downloading pictures from r/' + subreddit + '..')

    data = response.json()['data']['children']
    try:
        get_pictures_from_subreddit(data, subreddit, location)
    except:
        print('getting pictures from r/' + subreddit + ' failed')
    erase_previous_line()

    print('Downloaded pictures from r/' + subreddit)
