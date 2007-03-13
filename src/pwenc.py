#!/usr/bin/env python

from PWEncGlobals import *
from FileEncDec import *
import sys , os , getopt , tempfile , getpass

__version__ = '$Id$'

def usage (exitCode=0):
    print 'Usage: pwenc [-h] [-k] -(e|d|t|s) <file>'
    print '\t-h,--help\tshow this help'
    print '\t-r,--remove\tkeep the original file in an encrypt/decrypt op'
    print '\t-e,--encrypt\tencrypt the file'
    print '\t-d,--decrypt\tdecrypt the file'
    print '\t-t,--edit\tedit the file'
    print '\t-s,--show\tshow the file in your pager'
    sys.exit(exitCode)

def setGlobalOpts (glbs):
    shortOpts = ':edtshr'
    longOpts = ['encrypt' , 'decrypt' , 'edit' , 'show' , 'help' , 'remove']
    try:
        optlist , filelist = getopt.getopt(sys.argv[1:] , shortOpts , longOpts)
    except getopt.GetOptError:
        usage(1)
    if len(filelist) > 1:
        usage(1)
    
    # since we have valid options, roll through them and set the globals
    for opt in optlist:
        if opt[0] == '-e' or opt[0] == '--encrypt':
            glbs.Action = PWEncGlobals.ACT_ENC
        if opt[0] == '-d' or opt[0] == '--decrypt':
            glbs.Action = PWEncGlobals.ACT_DEC
        if opt[0] == '-t' or opt[0] == '--edit':
            glbs.Action = PWEncGlobals.ACT_EDIT
        if opt[0] == '-s' or opt[0] == '--show':
            glbs.Action = PWEncGlobals.ACT_SHOW
        if opt[0] == '-h' or opt[0] == '--help':
            usage()
        if opt[0] == '-r' or opt[0] == '--remove':
            glbs.RemoveOriginal = True
    
    if len(filelist) == 1:
        glbs.DefaultFile = filelist[0]

def getPassword (glbs , fCrypt):
    password = getpass.getpass('Password: ')
    if glbs.Action == PWEncGlobals.ACT_ENC:
        password2 = getpass.getpass('Password Again: ')
        if password != password2:
            print 'Your passwords did not match, try again'
            getPassword(glbs , fCrypt)
    
    if len(password) < 4:
        print 'Your password must be at least 4 characters'
        getPassword(glbs , fCrypt)
        
    fCrypt.setPassword(password)
    
def answerIsYes (default=False):
    """
    Gets a Yes or No answer from user input and return True on yes and
    False on no
    """
    ans = raw_input()
    if ans.lower() == 'n' or ans.lower() == 'no':
        return False
    if ans.lower() == 'y' or ans.lower() == 'yes':
        return True
    return default

def findProg (progName , arrPaths):
    """
    Checks a given array of paths for progName
    
    Returns the entire path to progName on success, False on failure
    """
    for path in arrPaths:
        curPath = os.path.join(path , progName)
        if os.path.exists(curPath):
            return curPath    
    return False
    
def encrypt (glbs , fCrypt):
    if not os.path.isfile(glbs.DefaultFile):
        print 'No file, %s, to encrypt' % glbs.DefaultFile
        sys.exit(4)
    if os.path.isfile(glbs.DefaultEncFile):
        print 'File, %s, already exists! Overwrite? [No]',
        if not answerIsYes():
            sys.exit(5)
    
    fCrypt.setInFile(glbs.DefaultFile)
    fCrypt.encFile(glbs.DefaultEncFile)
    fCrypt.close()
 
    if glbs.RemoveOriginal:
        os.remove(glbs.DefaultFile)

def decrypt (glbs , fCrypt):
    if not os.path.isfile(glbs.DefaultEncFile):
        print 'No file, %s, to decrypt' % glbs.DefaultEncFile
        sys.exit(4)
    if os.path.isfile(glbs.DefaultFile):
        print 'File, %s, already exists! Overwrite? [No]',
        if not answerIsYes():
            sys.exit(5)
    
    fCrypt.setInFile(glbs.DefaultEncFile)
    fCrypt.decFile(glbs.DefaultFile)
    fCrypt.close()
    
    if glbs.RemoveOriginal:
        os.remove(glbs.DefaultEncFile)

def edit (glbs , fCrypt):
    print 'Not yet implemented'

def show (glbs , fCrypt):
    # Need to find the path to the pager
    try:
        path = os.environ['PATH']
    except KeyError:
        path = '/usr/local/bin:/usr/bin:/bin'
    
    try:
        pager = findProg(os.environ['PAGER'] , path.split(':'))
    except KeyError:
        pager = findProg('less' , path.split(':'))
    if not pager:
        print 'You do not have a PAGER environment variable set and I ' + \
              'can\'t find "less" in your PATH'
        sys.exit(2)
        
    # Check to see if the encrypted file exists
    if not os.path.isfile(glbs.DefaultEncFile):
        print 'The file, %s, does not exist for viewing' % \
                glbs.getDefaultEncFile()
        sys.exit(3)
    # It does, so we set it in the encryption instance
    fCrypt.setInFile(glbs.getDefaultEncFile())
    
    fhPager = os.popen(pager , 'w')
    fCrypt.decFile(fhPager)
    fCrypt.close()
        
def main ():
    glbs = PWEncGlobals()
    fCrypt = FileEncDec()
    setGlobalOpts(glbs)
    # get the password
    getPassword(glbs , fCrypt)
    
    # perform the correct action based upon the defined action
    if glbs.Action == PWEncGlobals.ACT_ENC:
        encrypt(glbs , fCrypt)
    elif glbs.Action == PWEncGlobals.ACT_DEC:
        decrypt(glbs , fCrypt)
    elif glbs.Action == PWEncGlobals.ACT_EDIT:
        edit(glbs , fCrypt)
    elif glbs.Action == PWEncGlobals.ACT_SHOW:
        show(glbs , fCrypt)
        
if __name__ == '__main__':
    main()