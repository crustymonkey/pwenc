#!/usr/bin/env python

from Crypto.Hash import MD5
from Crypto.Cipher import AES

__all__ = ['Decrypter']
__version__ = '$Id$'

class Decrypter:
    
    def __init__ (self , password=None , toDecrypt=None):
        self.toDecrypt = toDecrypt
        if password: 
            self.setPassword(password)
        else:
            self.pwHash = None
            self.aes = None
            
    def setToDecrypt (self , toDecrypt):
        if toDecrypt == None:
            return False
        self.toDecrypt = toDecrypt
        return True
    
    def getToDecrypt (self):
        return self.toDecrypt
    
    def setPassword (self , password):
        if not password:
            raise Exception , 'You must specify a password to use for ' + \
                              'encryption'
        self.oMd5 = MD5.new(password)
        self.pwHash = self.oMd5.hexdigest()
        self.aes = AES.new(self.pwHash , AES.MODE_ECB)
        
    def decrypt (self , toDecrypt=None):
        if not self.pwHash:
            raise Exception , 'You need to specify a password before you ' + \
                              'can encrypt your string'
        if not self.toDecrypt and not toDecrypt:
            raise Exception , 'You need to specify a string to decrypt'
        if toDecrypt != None:
            self.toDecrypt = toDecrypt
        
        return self.aes.decrypt(self.toDecrypt).rstrip('\0')
    
if __name__ == '__main__':
    from Encrypter import *
    import sys , os , getpass
    
    password = getpass.getpass("Enter a password: ")
    print
    print "A line of text to encrypt:",
    text = raw_input()
    print 'A second line of text to encrypt:',
    text2 = raw_input()
    
    enc = Encrypter(password , text)
    dec = Decrypter(password)
    
    enctext = enc.encrypt()
    enctext2 = enc.encrypt(text2)
    comEnctext = enctext + enctext2
    
    print '\nDecrypted text:',
    dectext = dec.decrypt(enctext)
    dectext2 = dec.decrypt(enctext2)
    comDectext = dec.decrypt(comEnctext)
    print 'Text 1: %s\nText 2: %s\nText Combined: %s\n' % (dectext , dectext2 ,
                                                     comDectext)