#!/usr/bin/env python

import os, sys, time, md5


def printUsage():
    print 'usage: lockdo.py command luncher_unique_id [luncher_common_id]'
    print
    print 'lockdo is used to execute shell commands, providing a file-based locking mechanism.'
    print 'To avoid execution of the same <command> by different threads or machines in the same'
    print 'time, each thread creates a `.lock_*` file in the current working directory based'
    print 'on <luncher_unique_id> and <luncher_common_id> to decide if it is its turn to start'
    print 'a <command>. If <luncher_common_id> is not provided - <command> is its default value.'
    print
    print 'Please report bugs to karol.kruzelecki@cern.ch'
    print

def hash(value):
    return md5.new(value).hexdigest()

def checkLock(lockFile, command):
    if not os.path.exists(lockFile): return None
    else:
        lock = file(lockFile, 'r')
        lockData = lock.readlines()
        if len(lockData) < 3: # file currently in use by someone else, but not saved yet
            return 'in use'
        lockData = lockData[2]
        lock.close()
        return lockData

def createLock(lockFile, command, uniqId):
    lock = file(lockFile, 'w')
    lock.writelines([command, os.linesep, uniqId, os.linesep, hash(uniqId)])
    lock.close()

def removeLock(lockFile, command):
    try:
        os.remove(lockFile)
    except OSError:
        pass

def lockdo(command, uniqId, commonId=None):
    if commonId == None: hashCmd = hash(command) # check if it's None - '' is different than None so '== None' is necessary
    else: hashCmd = hash(commonId)
    hashUniqId = hash(uniqId)
    lockFileName = '.lock_' + hashCmd
    while True:
        c = checkLock(lockFileName, command)
        if c == hashUniqId:
            os.system(command)
            removeLock(lockFileName, command)
            break
        elif c == None:
            createLock(lockFileName, command, uniqId)
            continue
        time.sleep(5)


if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        printUsage()
        sys.exit()
    if len(sys.argv) > 3: commonId = sys.argv[3]
    else: commonId = None
    lockdo(sys.argv[1], sys.argv[2], sys.argv[3])
