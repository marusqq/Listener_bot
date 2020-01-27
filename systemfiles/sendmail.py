#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module used to send mail when needed'''

#for sending mail
import smtplib, ssl

def sendInfo(mes, sender_mail, receiver_mail, passw, subject = None):
    '''this is used for sending a message to mail'''

    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email =  sender_mail 
    receiver_email = receiver_mail 
    password = passw



    message = """\
Subject: """ + subject + """
    \n""" + mes

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    return