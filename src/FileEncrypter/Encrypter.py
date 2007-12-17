#!/usr/bin/env python

from Crypto.Hash import MD5
from Crypto.Cipher import AES

__all__ = ['Encrypter']
__cvsversion__ ='$Id$'

class Encrypter:
    
    def __init__ (self , password=None , toEncrypt=None):
        self.toEncrypt = toEncrypt
        if password: 
            self.setPassword(password)
        else:
            self.password = None
            self.aes = None
            
    def setToEncrypt (self , toEncrypt):
        if toEncrypt == None:
            raise Exception , 'You must specify a value to encrypt'
        self.toEncrypt = toEncrypt
    
    def getToEncrypt (self):
        return self.toEncrypt
    
    def setPassword (self , password):
        if not password:
            raise Exception , 'You must specify a password to use for ' + \
                              'encryption'
        if len(password) > 32:
            self.password = password[:32]
        else:
            topad = 32 - len(password)
            self.password = password + ('\0' * topad)
        self.aes = AES.new(self.password , AES.MODE_ECB)
        
    def encrypt (self , toEncrypt=None):
        if not self.password:
            raise Exception , 'You need to specify a password before you ' + \
                              'can encrypt your string'
        if not self.toEncrypt and not toEncrypt:
            raise Exception , 'You need to specify a string to encrypt'
        if toEncrypt != None:
            self.toEncrypt = toEncrypt
        # Since AES encryption requires the string to be a multiple of 16
        # characters, we will pad with spaces for now, null bytes later
        pad = 16 - len(self.toEncrypt) % 16
        padded = self.toEncrypt
        if pad:
            padded += '\0' * pad
        
        return self.aes.encrypt(padded)