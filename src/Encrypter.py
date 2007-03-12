#!/usr/bin/env python

from Crypto.Hash import MD5
from Crypto.Cipher import AES

__all__ = ['Encrypter']
__revision__ ='$Id$'

class Encrypter:
    
    def __init__ (self , password=None , toEncrypt=None):
        self.toEncrypt = toEncrypt
        if password: 
            self.setPassword(password)
        else:
            self.pwHash = None
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
        self.pwHash = MD5.new(password).hexdigest()
        self.aes = AES.new(self.pwHash , AES.MODE_ECB)
        
    def encrypt (self , toEncrypt=None):
        if not self.pwHash:
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
            for i in range(pad):
                padded += '\0'
        
        return self.aes.encrypt(padded)