#!/usr/bin/python

import smtplib
import traceback
from email.mime.text import MIMEText

SMTP_SERVER = 'mail10.csx.com'

class EmailManager(object):
    
    SMTP_SERVER_ERR = 'Email Manager Error: Encountered an error while attempting to send an email.'

    def __init__(self, sender=None, receivers=None, subject=None, text=None, server=SMTP_SERVER):
        self.__sender = sender
        
        if not isinstance(receivers, list):
            self.__receivers = [receivers]
        else:
            self.__receivers = receivers
            
        self.__subject = subject
        self.__text = text
        self.__server = server
        
    def get_sender(self):
        return self.__sender
        
    def set_sender(self, sender):
        self.__sender = sender
        
    def get_receivers(self):
        return self.__receivers
        
    def set_receivers(self, receivers):
        if not isinstance(receivers, list):
            self.__receivers = [receivers]
        else:
            self.__receivers = receivers
            
    def add_receivers(self, receivers):
        if not isinstance(receivers, list):
            self.__receivers.append(receivers)
        else:
            self.__receivers += receivers
            
    def get_subject(self):
        return self.__subject
        
    def set_subject(self, subject):
        self.__subject = subject
        
    def get_text(self):
        return self.__text
        
    def set_text(self, text):
        self.__text = text
        
    def get_server(self):
        return self.__server
        
    def set_server(self, server):
        self.__server = server
        
    def __get_message(self):
        return self.__message
        
    def __create_message(self):
        self.__message = MIMEText(self.get_text())
        self.__message['Subject'] = self.get_subject()
        self.__message['From'] = self.get_sender()
        self.__message['To'] = ','.join(self.get_receivers())
        
    def send_email(self):
        self.__create_message()
    
        try:
            smtp_server = smtplib.SMTP(self.get_server())
            smtp_server.sendmail(self.get_sender(), self.get_receivers(), self.__get_message().as_string())
            smtp_server.quit()
        except:
            print(self.SMTP_SERVER_ERR)
            print(traceback.format_exc())