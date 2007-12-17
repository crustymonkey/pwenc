import sys
assert sys.version >= '2' , 'Install Python 2.0 or greater'

try:
    import Crypto.Hash
except:
    print """You need the python Crypto module to use this package.

You can download this package at: 
    http://www.amk.ca/files/python/crypto/pycrypto-2.0.1.tar.gz"""
    sys.exit(1)
    
from distutils.core import setup

# $Id$

def runSetup ():
    setup(name = 'pwenc',
          version = '0.1',
          author = 'Jay Deiman' ,
          author_email = 'jay@splitstreams.com' ,
          url = 'http://splitstreams.com' ,
          license = 'GPLv2' ,
          platforms = [ 'unix' ] ,
          description = 'Password file encrypter and decrypter' ,
          packages = ['FileEncrypter'] ,
          scripts = ['pwenc.py']
    )
    
if __name__ == '__main__':
    runSetup()