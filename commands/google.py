#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module for using google module'''

#using https://github.com/hardikvasa/google-images-download
#Thanks @hardikvasa

#importing the code
from google_images_download import google_images_download

#this is needed for message and mention parameters
from fbchat.models import Message, Mention

#for getting author name
import systemfiles.utility

#for random functions
import os

def google_photos(client, keywords, image_limit, thread_id, thread_type, author_id):
    '''main function to handle downloading from google'''

    #download photos
    download_photos(keywords, image_limit)
    
    #sent the photos to fb
    send_google_photos_to_fb(client, keywords, author_id, thread_id, thread_type)

    return

def download_photos(keywords, image_limit):
    '''downloads photos to specified directory'''

    #validation for idiots
    if int(image_limit) > 25:
        image_limit = 25

    #instantiate the class
    response = google_images_download.googleimagesdownload()

    arguments = {
        "keywords":keywords,
        "limit":image_limit,
        "print_urls":False
    }

    paths,errors = response.download(arguments)



def send_google_photos_to_fb(client, keywords, author_id, threadid, threadtype):
    '''sends photos from directory to facebook's thread, tags the author and also specifies what subreddit is used'''

    code_dir = 'C:/Users/marius.pozniakovas/Desktop/randomPyScripts/Listener_bot/downloads/' #+ 'downloaded_photos/google/' 
    google_photos_dir = code_dir + keywords
    google_photos = os.listdir(google_photos_dir)

    #if we have atleast one photo
    if len(google_photos) > 0:

        author_name = systemfiles.utility.get_name(client, author_id)

        #first what we did
        client.send(
            Message(text='Photos googled by: ' + author_name + ', ' + 
            str(len(google_photos)) + ' by keyword ' + keywords + ' shown below:', 

            mentions=[Mention(author_id, offset=19, length=len(author_name))]),
            thread_id=threadid,
            thread_type=threadtype,
        )
        
        #send all photos
        for photo in google_photos:
            
            client.sendLocalImage(
                google_photos_dir + '/' + photo,
                thread_id=threadid,
                thread_type=threadtype,
                )

        return 

    #if we have less than 1 photo
    else:
        #no photos was used
        client.send(
            Message(text='No photos found by keywords: ' + keywords), 
            thread_id=threadid,
            thread_type=threadtype,
        )

        return