#!/usr/bin/env python
#
# Auth: Ilias Tsitsimpis
#       (Summer Student)
# Date: August 2011
#
# Script to compare results from the test with the references ones
# (results stored from release versions)
# I takes 2 or 3 arguments (depending on the action)
#    the action to perform:
#        MemLive  -> memory leaks (doesn't need a reference file)
#        MemTotal -> total memory use for each function
#        Perf     -> time performance for each function
#    the test file
#    the reference file
#
######################################################################

import re
import sys
import locale

#---------------------------------------------------------------------
def getTotalProfile(fin):
    for line in fin:    # search the file for the Flat `self' profile
        if line.startswith("Flat profile (self"):
            break

    i = 1
    for line in fin:    # skip two more lines
        if i == 2:
            break;
        i = i+1

    retValue = list()   # the return value will be a list
    for line in fin:
        if line == "\n":    # continue until find an empty line
            break
        temp = re.match(r"\s*(?P<total>\S+)\s+(?P<self>\S+)\s+(?P<calls>\S+)\s+(?P<function>.+) \[\d+\]", line) # split the line in (total :: self :: calls :: function) components using pattern matching
        if not temp:
            fin.close()
            print >> sys.stderr, ("(EE)  getTotalProfile: error in parsing the file")
            sys.exit(1)
        newValue = temp.groupdict()
        # we have to change `self' from string to long
        newValue['self'] = long(re.sub(r"\'", "", newValue['self']))
        retValue.append(newValue)

    return retValue

#---------------------------------------------------------------------
def getLiveProfile(fin):
    for line in fin:    # search the file for the Flat `cumulative' profile
        if line.startswith("Flat profile (cumulative"):
            break

    i = 1
    for line in fin:    # skip two more lines
        if i == 2:
            break;
        i = i+1

    retValue = list()   # the return value will be a list
    for line in fin:
        if line == "\n":    # continue until find an empty line
            break
        temp = re.match(r"\s*(?P<total>\S+)\s+(?P<self>\S+)\s+(?P<calls>\S+)\s+(?P<function>.+) \[\d+\]", line) # split the line in (total :: self :: calls :: function) components using pattern matching
        if not temp:
            fin.close()
            print >> sys.stderr, ("(EE)  getLiveProfile: error in parsing the file")
            sys.exit(1)
        newValue = temp.groupdict()
        # we have to change `self' from string to long
        newValue['self'] = long(re.sub(r"\'", "", newValue['self']))
        retValue.append(newValue)
        break

    return retValue

#---------------------------------------------------------------------
def getPerfProfile(fin):
    for line in fin:    # search the file for the Flat `self' profile
        if line.startswith("Flat profile (self"):
            break

    i = 1
    for line in fin:    # skip two more lines
        if i == 2:
            break;
        i = i+1

    retValue = list()   # the return value will be a list
    for line in fin:
        if line == "\n":    # continue until find an empty line
            break
        # split the line in (total :: self :: function) components using pattern matching
        temp = re.match(r"\s*(?P<total>\S+)\s+(?P<self>\S+)\s+(?P<function>.+) \[\d+\]", line)
        if not temp:
            fin.close()
            print >> sys.stderr, ("(EE)  getPerfProfile: error in parsing the file")
            sys.exit(1)
        newValue = temp.groupdict()
        # we have to change `self' from string to float
        newValue['self'] = float(newValue['self'])
        retValue.append(newValue)

    return retValue

#---------------------------------------------------------------------
def analyseMemTotal():
    for t in testData:  # for every function in test file
        found = False
        for r in refData:   # search every function in reference file
            if t['function'] != r['function']:
                continue    # if not the same continue searching

            # we found our function in reference file
            if (t['self'] > (1.05 * r['self'])):
                # if the differnce between the two is above 5% then FAIL
                print >> sys.stderr, ("(MEM) Total Memory: Function `%s' uses %ld memory but in refernce file used %ld" % (t['function'], t['self'], r['self']))
            found = True
            break

        if (not found) and (t['self'] > 500000):
            # we didn't find our function in reference file (a new function??)
            print >> sys.stderr, ("(NEW) Total Memory: Function `%s' not in the reference file" % t['function'])

#---------------------------------------------------------------------
def analysePerformance():
    for t in testData:  # for every function in test file
        found = False
        for r in refData:   # search every function in reference file
            if t['function'] != r['function']:
                continue    # if not the same continue searching

            # we found our function in refernce file
            if (t['self'] > (1.05 * r['self'])) and (t['self'] > 0.02):
                # if the difference between the two is above 5% then FAIL
                print >> sys.stderr, ("(PRF) Performance : Function `%s' runs in %f secs but in reference file in %f secs" % (t['function'], t['self'], r['self']))
            found = True
            break

        if (not found) and (t['self'] > 0.02):
            # we didn't find our function in reference file (a new function??)
            print >> sys.stderr, ("(NEW) Performance : Function `%s' not in the reference file" % t['function'])

#---------------------------------------------------------------------
def analyseMemLive():
    if testData and (testData[0]['self'] > 1000000):
        # if the first function (<spontaneous>) leaks more than 1 MB then FAIL
        print >> sys.stderr, ("(MEM) Live Memory : Program leaks %s bytes" % locale.format("%ld", testData[0]['self'], grouping=True))


#---------------------------------------------------------------------
locale.setlocale(locale.LC_ALL, 'en_US')
if len(sys.argv)==3 and sys.argv[1]=="MemLive":     # MemLive
    try:
        testFile = open(sys.argv[2], 'r')
    except IOError:
        print >> sys.stderr, ("(EE)  Could not open TEST file %s" % sys.argv[2])
        sys.exit(1)

    testData = getLiveProfile(testFile)
    testFile.close()
    analyseMemLive()
elif len(sys.argv)==4:
    # Open test and reference files
    try:
        refFile = open(sys.argv[3], 'r')
    except IOError:
        print >> sys.stderr, ("(WW)  Could not open REFERENCE file %s" % sys.argv[3])
        sys.exit(0)
    try:
        testFile = open(sys.argv[2], 'r')
    except IOError:
        refFile.close()
        print >> sys.stderr, ("(EE)  Could not open TEST file %s" % sys.argv[2])
        sys.exit(1)
    if sys.argv[1]=="MemTotal":                     # MemTotal
        refData = getTotalProfile(refFile)
        refFile.close()
        testData = getTotalProfile(testFile)
        testFile.close()
        analyseMemTotal()
    elif sys.argv[1]=="Perf":                       # Performance
        refData = getPerfProfile(refFile)
        refFile.close()
        testData = getPerfProfile(testFile)
        testFile.close()
        analysePerformance()
    else:                                           # Unkown action
        refFile.close()
        testFile.close()
        print ("(EE)  analyseIgprof.py: Unknown action %s" % sys.argv[1])
        sys.exit(1)
else:                                               # Wrong arguments
    print "(EE)  analyseIgprof.py: Wrong arguments"
    sys.exit(1)
