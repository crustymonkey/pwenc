#!/usr/bin/env python

"""
This is a script designed to take an input file and encrypt, 
decrypt, show or edit the file.  It uses an MD5 password hashing
plus AES encryption for the file.  You can set your default, 
unencrypted, filename at the top of this file.

Use "pwenc.py -h" to show the help for command-line operations
"""

# Change to your default unencrypted file path
DEFAULT_FILE = '/home/jdeiman/private/passwords'

######################################
#      DO NOT EDIT BELOW HERE        #
######################################

from FileEncrypter import FileEncDec , PWEncGlobals
import sys , os , getopt , tempfile , getpass

__cvsversion__ = '$Id$'
__all__ = ['usage' , 'setGlobalOpts' , 'getPassword' , 'answerIsYes' ,
           'findProg' , 'encrypt' , 'decrypt' , 'edit' , 'show' , 'main']

def usage (exitCode=0):
    """ Simply shows the help text if given a -h arg """
    print 'Usage: pwenc [-h] [-k] -(e|d|t|s) [<file>]'
    print '\t-h,--help\tshow this help'
    print '\t-k,--keep\tkeep the original file in an encrypt/decrypt op'
    print '\t-e,--encrypt\tencrypt the file'
    print '\t-d,--decrypt\tdecrypt the file'
    print '\t-t,--edit\tedit the file in your EDITOR'
    print '\t-s,--show\tshow the file in your PAGER'
    print """If <file> is not supplied, the DEFAULT_FILE from the top of the
pwenc.py file will be used.  You can open this file and change 
that variable to make operations faster.  Once this is set to the
path to your UNENCRYPTED file, you can use just type "pwenc.py -s"
or -e, etc., to show the file.
"""

    print 'You can type "pydoc pwenc" for more information'
    sys.exit(exitCode)

def setGlobalOpts (glbs):
    """
    Sets the global options from what is input on the command-line.  You
    can use "pwenc.py -h" to show the usage for the command-line ops
    """
    shortOpts = ':edtshk'
    longOpts = ['encrypt' , 'decrypt' , 'edit' , 'show' , 'help' , 'keep']
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
        if opt[0] == '-k' or opt[0] == '--keep':
            glbs.RemoveOriginal = False
    
    if len(filelist) == 1:
        glbs.DefaultFile = filelist[0]

def getPassword (glbs , fCrypt):
    """ Retrieves the password from the user and hashes it for use later """
    password = getpass.getpass('Passphrase: ')
    if glbs.Action == PWEncGlobals.ACT_ENC:
        password2 = getpass.getpass('Passphrase Again: ')
        if password != password2:
            print 'Your passphrases did not match, try again'
            getPassword(glbs , fCrypt)
    
    if len(password) < 4:
        print 'Your passphrase must be at least 4 characters'
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
    """ The function which encrypts your file """
    if not os.path.isfile(glbs.DefaultFile):
        print 'No file, %s, to encrypt' % glbs.DefaultFile
        sys.exit(4)
    if os.path.isfile(glbs.DefaultEncFile):
        print 'File, %s, already exists! Overwrite? [No]',
        if not answerIsYes():
            sys.exit(5)
    
    fCrypt.setInFile(glbs.DefaultFile)
    fCrypt.encFile(glbs.DefaultEncFile , glbs.FileHead)
    fCrypt.close()
 
    if glbs.RemoveOriginal:
        os.remove(glbs.DefaultFile)

def decrypt (glbs , fCrypt):
    """ The function which decrypts your file """
    if not os.path.isfile(glbs.DefaultEncFile):
        print 'No file, %s, to decrypt' % glbs.DefaultEncFile
        sys.exit(4)
    if os.path.isfile(glbs.DefaultFile):
        print 'File, %s, already exists! Overwrite? [No]',
        if not answerIsYes():
            sys.exit(5)
    
    fCrypt.setInFile(glbs.DefaultEncFile)
    if not fCrypt.checkPass(glbs.FileHead):
            print 'Passphrase incorrect'
            sys.exit(10)
    fCrypt.decFile(glbs.DefaultFile)
    fCrypt.close()
    
    if glbs.RemoveOriginal:
        os.remove(glbs.DefaultEncFile)

def edit (glbs , fCrypt):
    """
    This method writes the encrypted file to a temp file for writing, then
    it replaces the original encrypted file with the newly edited one
    """
    # Need to figure out the editor here to use
    try:
        path = os.environ['PATH']
    except KeyError:
        path = '/usr/local/bin:/usr/bin:/bin'
    try:
        editor = findProg(os.environ['EDITOR'] , path.split(':'))
    except KeyError:
        # default to vi
        editor = findProg('vi' , path.split(':'))
    if not editor:
        print 'You do not have a EDITOR environment variable set and I ' + \
              'can\'t find "vi" in your PATH'
        sys.exit(2)
    fCrypt.setInFile(glbs.DefaultEncFile)
    if not fCrypt.checkPass(glbs.FileHead):
        print 'Passphrase incorrect'
        sys.exit(10)
    # Create the temp file
    (tmpFd , tmpName) = tempfile.mkstemp('.tmp' , 'PW_')
    # First decrypt the file to a temp file
    fCrypt.decFile(tmpFd)
    fCrypt.close()
    cmd = '%s %s' % (editor , tmpName)
    # Now execute the user's editor to edit the temp file
    os.system(cmd)
    # Now encrypt the temp file to the original
    fCrypt.setInFile(tmpName)
    fCrypt.encFile(glbs.DefaultEncFile , glbs.FileHead)
    fCrypt.close()
    # And finally, remove the temp file
    os.remove(tmpName)

def show (glbs , fCrypt):
    """
    This will decrypt the file to memory and open the decrypted file for
    viewing in whatever you have set in your environment as PAGER.  If no
    environment variable, PAGER, is found, "less" is used as the default
    """
    # Need to find the path to the pager
    try:
        path = os.environ['PATH']
    except KeyError:
        path = '/usr/local/bin:/usr/bin:/bin'
    
    try:
        pager = findProg(os.environ['PAGER'] , path.split(':'))
    except KeyError:
        # default to less
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
    fCrypt.setInFile(glbs.DefaultEncFile)
    if not fCrypt.checkPass(glbs.FileHead):
            print 'Passphrase incorrect'
            sys.exit(10)
    
    fhPager = os.popen(pager , 'w')
    fCrypt.decFile(fhPager)
    fCrypt.close()
        
def main ():
    """
    The main function for the program.  Sets up objects and performs the
    requested action
    """
    global DEFAULT_FILE
    glbs = PWEncGlobals(defaultFile=DEFAULT_FILE)
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