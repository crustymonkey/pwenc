#!/usr/bin/env python

import sys , os , re

__all__ = ['InvalidFileException' , 'NoGPGException' , 'EncStateException' ,
           'GPGErrorException' , 'GPGFileEncrypter']

class InvalidFileException(Exception): pass

class NoGPGException(Exception): pass

class EncStateException(Exception): pass

class GPGErrorException(Exception): pass

class GPGFileEncrypter:    
    """ 
    This exists as a method to use an external GPG program to
    encrypt files and allow for the editing of said files
    """
    def __init__(self , filename , gpgId , gpgProg=None):
        # First check for a passed in path to GPG
        if gpgProg and os.path.isfile(gpgProg):
            self.gpgProg = gpgProg
        # If we didn't get one passed in, search the PATH var for it
        else:
            # Search the path for the gpg program
            self.gpgProg = self.findProg('gpg' , os.environ['PATH'].split(':'))
        # No GPG to be found
        if not self.gpgProg:
            raise NoGPGException , 'You need to install GPG'
        
        if not os.path.isfile(filename):
            raise InvalidFileException , filename
        self.filename = filename
        m = re.search('^(.+?)\.gpg$' , filename)
        if m:
            self.encFilename = filename
            self.baseFilename = m.group(1)
        else:
            self.encFilename = '%s.gpg' % filename
            self.baseFilename = filename
        self.gpgId = gpgId
        
    def findProg (self , progName , arrPaths):
        """
        Checks a given array of paths for progName
        
        Returns the entire path to progName on success, False on failure
        """
        for path in arrPaths:
            curPath = os.path.join(path , progName)
            if os.path.exists(curPath):
                return curPath    
        return False
    
    def encrypt (self):
        """
        Encrypts the file that was passed in to the constructor provided
        that it is not already encrypted
        """
        if os.path.isfile(self.encFilename):
            raise EncStateException , '%s is already encrypted' % \
                                    self.encFilename
        if not os.path.isfile(self.baseFilename):
            raise InvalidFileException , '%s does not exist to be encrypted' % \
                                       self.baseFilename
        sys.stderr.write('Encrypting\n')
        cmd = '%s -e -r %s %s' % (self.gpgProg , self.gpgId , self.baseFilename)
        status = os.system(cmd)
        if status:
            raise GPGErrorException , \
                                'A problem occured encrypting the file: %s' \
                                % self.baseFilename
        os.remove(self.baseFilename)
        sys.stderr.write('The file, %s, was successfully encrypted as %s\n' %
                         (self.baseFilename , self.encFilename))
        return True
    
    def decrypt (self):
        """
        Decrypts the file that was passed in to the constructor provided
        that it is not already encrypted
        """
        if os.path.isfile(self.baseFilename):
            raise EncStateException , '%s is already decrypted' % \
                                    self.baseFilename
        if not os.path.isfile(self.encFilename):
            raise InvalidFileException , '%s does not exist to be decrypted' % \
                                       self.encFilename
        sys.stderr.write('Decrypting\n')
        cmd = '%s -d --output %s %s' % (self.gpgProg , self.baseFilename ,
                                        self.encFilename)
        status = os.system(cmd)
        if status:
            raise GPGErrorException , \
                                'A problem occured decrypting the file: %s' \
                                % self.encFilename
        os.remove(self.encFilename)
        sys.stderr.write('The file, %s, was successfully decrypted as %s\n' %
                         (self.encFilename , self.baseFilename))
        return True
    
    def getContents (self , getArray=False):
        """
        Gets the contents of either the file that is in an ecrypted or
        decrypted state
        """
        if os.path.isfile(self.baseFilename) and \
                os.path.isfile(self.encFilename):
            raise InvalidFileException('Both an encrypted and decrypted' +
                                       'version of the file, %s, exist' %
                                       (self.baseFilename))
        elif os.path.isfile(self.baseFilename):
            fh = open(self.baseFilename , 'r')
            if getArray:
                lines = fh.readlines()
                fh.close()
                return lines
            else:
                bytes = fh.read()
                fh.close()
                return bytes
        elif os.path.isfile(self.encFilename):
            ret = None
            try:
                self.decrypt()
                fh = open(self.baseFilename , 'r')
                if getArray:
                    ret = fh.readlines()
                else:
                    ret = fh.read()
                fh.close()
                self.encrypt()
            except:
                raise
            
            return ret
        
        # We got to here and we shouldn't have, toss an exception
        emsg = 'Neither the file, %s, nor the file, %s, exists!' % \
                (self.encFilename , self.baseFilename)
        raise InvalidFileException , emsg
    
if __name__ == '__main__':
    # do something
    passfile = GPGFileEncrypter(sys.argv[1] , sys.argv[2])
    print passfile.getContents()