#!/usr/bin/env python
"""
$Id$
"""

from GPGFileEncrypter import *
import os , sys

class EncFileManager (GPGFileEncrypter):
    def __init__ (self , filename , gpgId , gpgProg=None):
        GPGFileEncrypter.__init__(self , filename , gpgId , gpgProg)
        
    def view (self):
        lPipe = os.popen('less' , 'w')
        lPipe.write(self.getContents())
        lPipe.close()
        

if __name__ == '__main__':
    passfile = EncFileManager(sys.argv[1] , sys.argv[2])
    passfile.view()