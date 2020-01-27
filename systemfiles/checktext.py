#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module analyzing what command should be used'''

#import the commands which can be used
import commands.reddit
import commands.info
import commands.basic_reply

#for os functions
import os

#importing systemfiles
    #for random utilities
import systemfiles.utility

#for mention and message
from fbchat.models import Message, Mention



def decide(client, message, thread_id, thread_type, author_id):
    '''function that decides what job to do, if None, returns False'''

    #if we don't find any command we return false
    command_found = False

    words = message.split()

    for i in range(0, len(words)):

        if i == 0 and words[i] == '!topreddit':

            #check if there is atleast 4 words
            if not len(words) < 3:
                
                if (words[i+2] == 'day' or words[i+2] == 'week' or
                words[i+2] == 'month' or words[i+2] == 'year' or 
                words[i+2] == 'all') and words[i+3].isdigit():

                    #send to command if everything is ok
                    command_found = True
                    commands.reddit.get_and_send_photos_from_reddit(
                        client, 
                        words[i+1], words[i+2], words[i+3],
                        thread_id, thread_type,
                        author_id
                    )

                    #delete the downloaded files
                    systemfiles.utility.delete_dir(str(os.getcwd()) + '/reddit/' + words[i+1] + '/')
                    systemfiles.log.log(author_id, '!topreddit used')

                    i = i + 3

                #not day/week/month/year/all or image_count not a number:
                else:
                    client.send(
                    Message(text = 'Usage: ![topreddit] [subreddit] [day/week/month/year/all] [image_count]'), 
                    thread_id = thread_id, 
                    thread_type = thread_type
                    )

            #less than 4 words:
            else:
                #send the usage
                client.send(
                    Message(text = 'Usage: ![topreddit] [subreddit] [day/week/month/year/all] [image_count]'), 
                    thread_id = thread_id, 
                    thread_type = thread_type
                )

        elif i == 0 and words[i] == '!help':
            command_found = True
            systemfiles.log.log(author_id, '!help used')
            commands.info.help(client, thread_id, thread_type)

        elif i == 0 and words[i] == '!info':
            command_found = True
            systemfiles.log.log(author_id, '!info used')
            commands.info.documentation(client, thread_id, thread_type)
            
        elif i == 0 and words[i] == '!ideas':
            command_found = True
            systemfiles.log.log(author_id, '!ideas used')
            commands.info.ideas(client, thread_id, thread_type)
        
        elif words[i] == '2iq':
            command_found = True
            systemfiles.log.log(author_id, '2iq printed')
            commands.basic_reply.two_iq(client, thread_id, thread_type)

        elif words[i] == 'lexus':
            command_found = True
            systemfiles.log.log(author_id, 'lexus used')
            commands.basic_reply.lexus(client, thread_id, thread_type)

        elif words[i] == 'fat' or words[i] == 'storas':
            command_found = True
            systemfiles.log.log(author_id, 'fat used')
            commands.basic_reply.fat(client, thread_id, thread_type)

        elif words[i] == 'lenkas':
            command_found = True
            systemfiles.log.log(author_id, 'lenkas used')
            commands.basic_reply.polish(client, thread_id, thread_type)
        
        elif words[i] == 'lenkas' and author_id == '100001826192111':
            command_found = True
            systemfiles.log.log(author_id, 'bmw used')
            commands.basic_reply.bmw(client, thread_id, thread_type)

        elif words[i] == 'nigger' or words[i] == 'nigeri' or words[i] == 'nigeris':
            command_found = True
            systemfiles.log.log(author_id, 'N word said')
            commands.basic_reply.n_patrol(client, thread_id, thread_type)
    
    return command_found