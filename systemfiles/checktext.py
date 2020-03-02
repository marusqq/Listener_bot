#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module analyzing what command should be used'''

#import the commands which can be used
import commands.reddit
import commands.info
import commands.basic_reply
import commands.log
import commands.google

#for os functions
import os

#importing systemfiles
    #for random utilities
import systemfiles.utility

#for mention and message
from fbchat.models import Message, Mention



def decide(client, message, thread_id, thread_type, author_id):
    '''function that decides what job to do, if None, returns False'''

    #get the name of the author_id for better information usage
    author_name = systemfiles.utility.get_name(client, author_id)


    #if we don't find any command we return false
    command_found = False

    if message is None:
        words = []
    else:
        words = message.split()

    for i in range(0, len(words)):

        if author_id != '100047885599974':

            if i == 0 and words[i] == '!reddit':

                #check if there is atleast 4 words
                if not len(words) < 4:
                    
                    if (words[i+2] == 'day' or words[i+2] == 'week' or
                    words[i+2] == 'month' or words[i+2] == 'year' or 
                    words[i+2] == 'all') and words[i+3].isdigit() and words[i+3] != '0':

                        #send to command if everything is ok
                        command_found = True
                        systemfiles.log.log(author_name, '!reddit ' + str(words[i+1]) + ' ' + str(words[i+2]) + ' ' + str(words[i+3]) + ' used')
                        commands.reddit.get_and_send_photos_from_reddit(
                            client, 
                            words[i+1], words[i+2], words[i+3],
                            thread_id, thread_type,
                            author_id
                        )

                        #delete the downloaded files
                        systemfiles.utility.delete_dir(str(os.getcwd()) + '/reddit/' + words[i+1] + '/')

                        #skip few words
                        i = i + 4

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
                        Message(text = 'Usage: !topreddit [subreddit] [day/week/month/year/all] [image_count]'), 
                        thread_id = thread_id, 
                        thread_type = thread_type
                    )

            elif i == 0 and words[i] == '!google':

                #check if we have enough words for keyword and image_limit
                if not len(words) < 3:
                    
                    #check image_limit
                    if words[i+2].isdigit() and words[i+2] != '0':

                        command_found = True
                        #log it
                        systemfiles.log.log(author_name, '!google ' + str(words[i+1]) + ' ' + str(words[i+2]) + ' used')
                        
                        #do it
                        commands.google.google_photos(
                            client, 
                            words[i+1], words[i+2],
                            thread_id, thread_type,
                            author_id
                        )

                        #delete files
                        systemfiles.utility.delete_dir(str(os.getcwd()) + '/downloads/' + words[i+1] + '/')

                        #skip words then
                        i = i + 3
                    
                    else:
                        #send the usage
                        client.send(
                            Message(text = 'Make sure [image_count] is a number and is more than 0'), 
                            thread_id = thread_id, 
                            thread_type = thread_type
                        )
                
                #less than 3 words
                else:
                    #send the usage
                    client.send(
                        Message(text = 'Usage: !google [keyword] [image_count]'), 
                        thread_id = thread_id, 
                        thread_type = thread_type
                    )

                
            elif i == 0 and words[i] == '!help':
                command_found = True
                systemfiles.log.log(author_name, '!help used')
                commands.info.help(client, thread_id, thread_type)

            elif i == 0 and words[i] == '!info':
                command_found = True
                systemfiles.log.log(author_name, '!info used')
                commands.info.documentation(client, thread_id, thread_type)
                
            elif i == 0 and words[i] == '!ideas':
                command_found = True
                systemfiles.log.log(author_name, '!ideas used')
                commands.info.ideas(client, thread_id, thread_type)

            elif i == 0 and words[i] == '!log' and words[i+1].isdigit() and words[i+2] == 'passw':
                command_found = True

                #systemfiles.log.log(author_name, '!log ' + str(words[i+1]) + ' used')
                #dont log this probably :D
                
                commands.log.get_log(client, thread_id, thread_type, words[i+1])

                #now skip one word
                i = i + 2
            
            elif words[i] == '2iq':
                command_found = True
                systemfiles.log.log(author_name, '2iq printed')
                commands.basic_reply.two_iq(client, thread_id, thread_type)

            elif words[i] == 'lexus':
                command_found = True
                systemfiles.log.log(author_name, 'lexus used')
                commands.basic_reply.lexus(client, thread_id, thread_type)

            elif words[i] == 'fat' or words[i] == 'storas':
                command_found = True
                systemfiles.log.log(author_name, 'fat used')
                commands.basic_reply.fat(client, thread_id, thread_type)

            elif words[i] == 'lenkas':
                command_found = True
                systemfiles.log.log(author_name, 'lenkas used')
                commands.basic_reply.polish(client, thread_id, thread_type)
            
            elif words[i] == 'lenkas' and author_id == '100001826192111':
                command_found = True
                systemfiles.log.log(author_name, 'bmw used')
                commands.basic_reply.bmw(client, thread_id, thread_type)

            elif words[i] == 'nigger' or words[i] == 'nigeri' or words[i] == 'nigeris':
                command_found = True
                systemfiles.log.log(author_name, 'N word said')
                commands.basic_reply.n_patrol(client, thread_id, thread_type)
    
    return command_found