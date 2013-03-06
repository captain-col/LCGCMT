#!/usr/bin/env python

# @file: GaudiPolicy/cmt/fragments/merge_files.py
# @purpose: merge_files <fragment> file into a 'per-project' <merged> file
# @author: Sebastien Binet <binet@cern.ch>

import os
import sys
from datetime import datetime
import locker
    
def mergeFiles( fragFileName, mergedFileName, commentChar, doMerge ):

    isNewFile = not os.path.exists(mergedFileName)
    
    # create an empty file if it does not exist
    if isNewFile: open(mergedFileName,'w')
    
    mergedFile = open( mergedFileName, 'r+' )

    # locking file, gaining exclusive access to it
    lock = locker.lock( mergedFile, locker.LOCK_EX )

    startMark = "%s --Beg %s" % ( commentChar,
                                  os.path.basename(fragFileName) )
    timeMark  = "%s --Date inserted: %s" % ( commentChar,
                                             str(datetime.now()) )
    endMark   = "%s --End %s" % ( commentChar,
                                  os.path.basename(fragFileName) )

    newLines = [ ]
    skipBlock = False
    for line in mergedFile.readlines():
        if line.startswith(startMark):
            skipBlock = True
            # remove all the empty lines occurring before the start mark
            while (len(newLines) > 0) and (newLines[-1].strip() == ''):
                newLines.pop()
        if not skipBlock:
            newLines.append(line)
        if line.startswith(endMark):
            skipBlock = False
    if skipBlock:
        print "WARNING: missing end mark ('%s')"%endMark
    
    if doMerge:
        # I do not want to add 2 empty lines at the beginning of a file
        if not isNewFile:
            newLines.append('\n\n')
        newLines.append(startMark+'\n')
        newLines.append(timeMark+'\n')
    
        for line in open( fragFileName, 'r' ).readlines():
            newLines.append(line)
        
        newLines.append(endMark+'\n')
    
    mergedFile.seek(0)
    mergedFile.truncate(0)
    mergedFile.writelines(newLines)
    
    return 0

if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option(
        "-i",
        "--input-file",
        dest = "fragFileName",
        default = None,
        help = "The path and name of the file one wants to merge into the 'master' one"
        )
    parser.add_option(
        "-m",
        "--merged-file",
        dest = "mergedFileName",
        default = None,
        help = "The path and name of the 'master' file which will hold the content of all the other fragment files"
        )
    parser.add_option(
        "-c",
        "--comment-char",
        dest = "commentChar",
        default = "#",
        help = "The type of the commenting character for the type of files at hand (this is an attempt at handling the largest possible use cases)"
        )
    parser.add_option(
        "--do-merge",
        dest = "doMerge",
        action = "store_true",
        default = True,
        help = "Switch to actually carry on with the merging procedure"
        )
    parser.add_option(
        "--un-merge",
        dest = "unMerge",
        action = "store_true",
        default = False,
        help = "Switch to remove our fragment file from the 'master' file"
        )
    
    (options, args) = parser.parse_args()

    # ensure consistency...
    options.doMerge = not options.unMerge

    sc = 1
    if not options.fragFileName or \
       not options.mergedFileName :
        str(parser.print_help() or "")
        print "*** ERROR ***"
        sys.exit(sc)
        pass

    #stampFileName  = options.fragFileName + ".stamp"
    stampFileName = os.path.join(os.path.dirname(options.mergedFileName),
                                 os.path.basename(options.fragFileName)) + ".stamp"
    try:
        sc = mergeFiles( options.fragFileName, options.mergedFileName,
                         options.commentChar,
                         doMerge = options.doMerge )
        stamp = open( stampFileName, 'w' )
        stamp.close()
    except IOError, err:
        print "ERROR:",err
    except Exception, err:
        print "ERROR:",err
    except:
        print "ERROR: unknown error !!"

    sys.exit( sc )
