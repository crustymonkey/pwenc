#!/usr/bin/env python

from FileEncDec import *
import getopt , os , sys , re

__all__ = ['InvalidAction' , 'PWEncGlobals']
__version__ = '$Id$'

class InvalidAction (Exception): pass

# Globals
class PWEncGlobals (object):
    ACT_SHOW = 1
    ACT_ENC = 2
    ACT_DEC = 4
    ACT_EDIT = 8
    ENC_FILE_EXT = '.enc'
    def __init__ (self , action=0 , defaultFile=''):
        try:
            self.setAction(action)
        except InvalidAction:
            self._action = self.ACT_SHOW
        
        try:
            self.setDefaultFile(defaultFile)
        except InvalidFileException:
            self._defaultFile = '/home/jdeiman/private/passwords'
            self._defaultEncFile = self._defaultFile + self.ENC_FILE_EXT
            
        self._removeOriginal = False
        
    def getAction (self):
        return self._action
    
    def setAction (self , action):
        if type(action) == type(1):
            # check to make sure it is one of the valid action types
            allActions = self.ACT_DEC | self.ACT_ENC | self.ACT_EDIT | \
                         self.ACT_SHOW
            if action & allActions:
                self._action = action
                return
        # If we get here, we have a problem
        raise InvalidAction , 'The action, %s, is invalid' % action
    
    def getDefaultFile (self):
        return self._defaultFile
    
    def getDefaultEncFile (self):
        return self._defaultEncFile
    
    def setDefaultFile (self , defaultFile):
        if defaultFile and os.path.isfile(defaultFile):
            pattern = '^(.*?)\\%s$' % self.ENC_FILE_EXT
            m = re.match(pattern , defaultFile)
            if m:
                self._defaultEncFile = defaultFile
                self._defaultFile = m.group(1)
            else:
                self._defaultFile = defaultFile
                self._defaultEncFile = defaultFile + self.ENC_FILE_EXT
            return
        # We shouldn't get here
        raise InvalidFileException , 'The default file, %s, is invalid' % \
                                      defaultFile
    def getRemoveOriginal (self):
        return self._removeOriginal
    
    def setRemoveOriginal (self , remove):
        if remove:
            self._removeOriginal = True
        else:
            self._removeOriginal = False
    
    Action = property(getAction , setAction)
    DefaultFile = property(getDefaultFile , setDefaultFile)
    DefaultEncFile = property(getDefaultEncFile , None)
    RemoveOriginal = property(getRemoveOriginal , setRemoveOriginal)
    
# testing
if __name__ == '__main__':
    glbs = PWEncGlobals()
    print glbs.Action
    print glbs.DefaultFile