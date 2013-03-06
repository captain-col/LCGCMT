'''
Date: june/29/2005                    
Description: Class and methods to use CMT with Python sources, based on the christian's python class.

Simple usage:
    import CMT

    if __name__ == "__main__":

        cmt = CMT()
    
        package = 'CMTpy'
    
        package_root = cmt.macro_value (package + '_root')    
        print  package_root
    
        if cmt.tag (package + '_with_installarea'):
            print package + ' strategy is with installarea'
    
        print "Macros: ", cmt.macros  , '\n'       
        print "Tags: ",   cmt.tags    , '\n' 
        print "Sets: ",   cmt.sets    , '\n'      
    
'''
__author__ = "Vincent Garonne"
__email__ = "garonne at lal dot in2p3 dot fr"
__version__ = "v1"
__all__     = ["CMT"]

import os
import sys
import string
import stat
import re
import commands
from os import path
from subprocess import *


#----------------------------------------------------
def execute(cmd):
    """Executing a shell command
    """
    
    (stdout, stderr) = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()
    
    lines = []
    for line in stdout.splitlines():
        lines.append(string.rstrip(line))
        
    return lines

class CMT:

    def __init__ (self):
        """Constructor
        """
        # __init__
        # Variables
        self.cmtexe   = os.environ ['CMTROOT'] + '/' + os.environ ['CMTBIN'] + '/cmt.exe -tag_add=Doxygen '
        self.macros   = dict ()
        self.tags     = dict ()
        self.sets     = dict ()
        self.uses     = []
        self.top_uses = []
        
        # Initialyzation
        self.init_sets ()
        self.init_macros ()
        self.init_tags ()
        self.init_uses ()

    def expand_pattern (self, text, p1, p2):
        v = text
        rexp = ''
        for c in p1:
            rexp += r'[' + c + r']'
        rexp += '([^' + p2 + r']*)[' + p2 + r']'
        while True:
            ms = re.findall (rexp, v)
            if len(ms) == 0:
                break
            for m in ms:
                if m in self.macros:
                    v = string.replace (v, p1 + m + p2, self.macros[m])
                elif m in os.environ:
                    v = string.replace (v, p1 + m + p2, os.environ [m])
                else:
                    v = string.replace (v, p1 + m + p2, '')
        # while True
        return (v)

    def expand (self, text):
        v = text
        v = self.expand_pattern (v, '$(', ')')
        v = self.expand_pattern (v, '${', '}')
        v = self.expand_pattern (v, '%', '%')
        return (v)
    # expand
    
    # Pre-fetch the macro values and expand all of them
    def init_macros (self):
        lines = execute (self.cmtexe + ' show macros')
        for line in lines:
            w = string.split (line, '=')
            name = w[0]
            if len(w)>=2:             
                 value = re.sub ('^[\']', '', w[1])
                 value = re.sub ('[\']$', '', value)
                 self.macros [name] = value
        for key in self.macros.keys():
            self.macros[key] = self.expand (self.macros[key])
            #print key + '=' + v
        # for key in self.macros.keys():
    # init_macros

    def init_sets (self):
        lines = execute (self.cmtexe + ' show sets')
        for line in lines:
            w = string.split (line, '=')
            name = w[0]
            if len(w)>=2:
                 value = re.sub ('^[\']', '', w[1])
                 value = re.sub ('[\']$', '', value)
                 self.sets [name] = value
        for key in self.sets.keys():
            self.sets[key] = self.expand (self.sets[key])
            #print key + '=' + v
        # for key in self.macros.keys():
    # init_sets

    def init_tags (self):
        lines = execute (self.cmtexe + ' show tags')
        for line in lines:
            w = string.split (line, ' ')
            name = w[0]
            #print 'tag=' + name
            self.tags [name] = True
    # init_tags

    def init_uses (self):
        lines = execute (self.cmtexe + ' show uses')
        for line in lines:
            if line[0] == '#':
                if line[0:5] == '# use':
                    w = string.split (line, ' ')
                    #print 'init_uses> [' + w[2] + ']'
                    self.top_uses.append (w[2])
                continue
            self.uses.append (line)
    # init_uses

    def macro_value (self, name):
        if not self.macros.has_key (name):
            return ''
        return self.macros[name]
    # macro_value

    def tag (self, name):
        if not self.tags.has_key (name):
            return False
        return True
    # tag

    def do (self, cmd):
        execute (self.cmtexe + ' ' + cmd)
    # do
    
##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":

    cmt = CMT()
    
    package = 'pyCMT'
    
    package_root = cmt.macro_value (package + '_root')    
    print  package_root
    
    if cmt.tag (package + '_with_installarea'):
        print package + ' strategy is with installarea'
    
    print "Macros: ", cmt.macros  , '\n'       
    print "Tags: ",   cmt.tags    , '\n' 
    print "Sets: ",   cmt.sets    , '\n'      

#--------------------------------- EoF --------------------------------------#
    
   
