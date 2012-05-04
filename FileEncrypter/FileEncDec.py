#!/usr/bin/env python

from Decrypter import Decrypter
from Encrypter import Encrypter
import os , sys

__all__ = ['FileNotSetException' , 'PassNotSetException' , 
           'InvalidFileException' , 'FileEncDec']
__cvsversion__ = '$Id$'

class FileNotSetException (Exception): pass
class PassNotSetException (Exception): pass
class InvalidFileException (Exception): pass

class FileEncDec (Decrypter , Encrypter):
    
    def __init__ (self , password=None , file=None):
        self.setInFile(file)
        Encrypter.__init__(self , password , None)
        Decrypter.__init__(self , password , None)
            
    def setInFile (self , file):
        """
        Set the intput file object
        """
        if file == None:
            return False
        oFile = self._getFObject(file)
        if oFile == None:
            return False
        
        self.oFile = oFile
        self.fdFile = oFile.fileno()
        return True
    
    def getInFileObject (self):
        """
        Returns the input file object
        """
        return self.oFile

    def setPassword (self , password):
        Encrypter.setPassword(self , password)
        Decrypter.setPassword(self , password)
        
    def _getFObject (self , file , mode='r'):
        if file == None:
            raise InvalidFileException , 'You must specify a file'
        # 'file' can be either a file object, file descriptor, or path to a file
        if str(type(file)).find('file') > -1:
            if not (file.mode.find(mode) > -1 or file.mode.find('+')):
                file.mode = mode
            return file
        elif type(file) == type(1):
            # We supposedly have a file descriptor, it's going to throw an
            # exception if the int is not actually a file desciptor
            try:
                fObject = os.fdopen(file , mode)
            except OSError:
                raise InvalidFileException , 'The integer does not refer ' + \
                                             'to a valid file descriptor'
            if not (fObject.mode.find(mode) > -1 or fObject.mode.find('+')):
                fObject.mode = mode
            return fObject
        elif type(file) == type('string'):
            try:
                fObject = open(file , mode)
            except IOError:
                err = 'The filename, %s, is not readable' % file
                raise InvalidFileException , err
            return fObject
        
        return None
    
    def _encDecFile (self , outFile , op , header=None):
        if self.oFile == None:
            raise FileNotSetException , 'You must set a file to be en/decrypted'
        if self.password == None:
            raise PassNotSetException , 'You must set a password to ' + \
                                        'en/decrypt the file'
        try:
            oOutFile = self._getFObject(outFile , 'w')
        except InvalidFileException:
            # Default to standard out if the outfile is invalid
            oOutFile = sys.stdout
        
        if op == self.encrypt:
            # Write the password hash at the beginning
            oOutFile.write(self.encrypt(header))
        else:
            # Read the first 16 bytes to bypass the password
            self.oFile.read(16) 
        while True:
            block = self.oFile.read()
            if not block:
                break
            oOutFile.write(op(block))
            oOutFile.flush()
        oOutFile.close()
        
    def encFile (self , outFile , header):
        """
        You must pass in either a filename, a file handle or a valid file
        descriptor (such as sys.stdout) to write the encryption output to.
        If a valid file is NOT passed in, the output will default to stdout
        """
        self._encDecFile(outFile, self.encrypt , header)

    def decFile (self , outFile):
        """
        You must pass in either a filename, a file handle or a valid file
        descriptor (such as sys.stdout) to write the decryption output to.
        If a valid file is NOT passed in, the output will default to stdout
        """
        self._encDecFile(outFile , self.decrypt)
    
    def checkPass (self , header):
        """
        Read the first 16 bytes of the file to get the password hash and
        compare them to the current hash
        """
        self.oFile.seek(0)
        eHead = self.oFile.read(16)
        head = self.aes.decrypt(eHead)
        if head == header:
            return True
        return False
        
    def close (self):
        if not self.oFile.closed:
            self.oFile.close()
    
# Testing
if __name__ == '__main__':
    fenc = None
    if sys.argv[1] == 'enc':
        fenc = FileEncDec(file='/home/jdeiman/writetest')
        fenc.setPassword('chicken')
        fenc.encFile('/home/jdeiman/encfile')
    elif sys.argv[1] == 'dec':
        fenc = FileEncDec(file='/home/jdeiman/encfile')
        fenc.setPassword('chicken')
        fenc.decFile(sys.stdout)
    fenc.close()   