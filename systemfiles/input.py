#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module for getting hardcoded data or inputing it in'''

#for secure password input
import getpass

def get_data(data_from_file):
    '''fill empty array with passwords and other sensitive data'''

    data_arr = []

    if data_from_file:
        
        with open('data.bin') as file:
            for line in file:
                line = line.rstrip()
                line = line.lstrip()
                data_arr.append(line)
        
        return data_arr

    #input by hand
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

        return data_arr