#!/usr/bin/env python
"""
$Id$
"""

from GPGFileEncrypter import *
import os , sys , tempfile

class EncFileManager (GPGFileEncrypter):
    def __init__ (self , filename , gpgId , gpgProg=None , quiet=False):
        GPGFileEncrypter.__init__(self , filename , gpgId , gpgProg , quiet)
        
    def view (self):
        """
        This will open the encrypted file and read it to memory.  Then it will
        pipe the contents to less for reading after reencrypting the file.
        """
        # Get the contents of the encrypted file
        contents = self.getContents()
        # Find less and dump the contents to it
        lessPath = self._findProg('less', os.environ['PATH'].split(':'))
        if not os.path.isfile(lessPath):
            raise InvalidFileException , 'Could not find "less" on your path'
        lPipe = os.popen(lessPath , 'w')
        lPipe.write(contents)
        lPipe.close()
        
    def edit (self):
        """
        A method that can be called to edit the file.  This will open and read
        the encryted file to memory and reencrypt the file.  After this, the
        contents will be written to a secure temp file for editing.  After
        quitting VI, the file will be moved to the unencrypted location and
        then encrypted.
        """
        # Read the contents of the current file
        contents = self.getContents()
        # Make a temp file  and write the contents to it
        (fh , tmpfile) = tempfile.mkstemp('.tmp', 'PW_', '/tmp')
        os.write(fh , contents)
        os.close(fh)
        # Get the path to VI
        viPath = self._findProg('vi' , os.environ['PATH'].split(':'))
        if not os.path.isfile(viPath):
            raise InvalidFileException , 'Could not find vi on your path'
        # Open the tempfile in vi
        cmd = '%s -n %s' % (viPath , tmpfile)
        os.system(cmd)
        # Move the temp file to the original directory
        os.rename(tmpfile, self.baseFilename)
        if os.path.isfile(self.encFilename): 
            # Remove the original encrypted file
            os.remove(self.encFilename)
        # And now encrypt it
        self.encrypt()
        
if __name__ == '__main__':
    passfile = EncFileManager(sys.argv[1] , sys.argv[2])
    passfile.edit()