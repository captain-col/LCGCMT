#!/usr/bin/env python

import os, sys
import re

def replaceLine(file, pat, sub) :

    print "replacing '" + pat + "' by '" + sub + "' in ", file

    inFile = open(file)
    lines = inFile.readlines()
    inFile.close()

    outFile = open(file,"w")
    for line in lines :
        newLine = re.sub(pat, sub, line)
        outFile.write(newLine)

    outFile.close()
    return

if (__name__ == "__main__") :

    if ( len(sys.argv) < 3 ) :
        print "usage: ", sys.argv[0]," <file> <pattern> <replacement> "
        sys.exit(0)

    else :

        inFileName = sys.argv[1]
        pat = sys.argv[2]
        sub = sys.argv[3]
        
        replaceLine(inFileName, pat, sub)
