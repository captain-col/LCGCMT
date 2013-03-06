#!/usr/bin/env python

#
# Auth: Ilias Tsitsimpis
#       (Summer Student)
# Date: August 2011
#
# Script to convert qmtest results for igprof
# from plain text to html file in order to add links to our results
#
# I takes 1 argument, the log file to convert into html
# then it generates a new file with the same name and .html as suffix
#
######################################################################


import re
import sys
import os

if len(sys.argv) != 2:
    print >> sys.stderr, "generateIgprof.py: Wrong arguments"
    sys.exit(1)

logName = os.path.splitext(sys.argv[1])[0]
logFile = open(sys.argv[1], 'r')
htmlFile = open(logName + '.html', 'w')

htmlFile.write("<html>\n<head>\n<title>Igprof Results</title>\n")
htmlFile.write("</head>\n<body>\n<pre>")
htmlFile.write("Markers: (MEM) failure in memory profiling\n")
htmlFile.write("               programm leaks memory or\n")
htmlFile.write("               a function uses more memory than in reference file\n")
htmlFile.write("         (PRF) failure in performance profiling\n")
htmlFile.write("               a function takes more time than in reference file\n")
htmlFile.write("         (NEW) a new function appears with (self >= 0.01%)\n")
htmlFile.write("\n")
htmlFile.write("         (WW) warning\n")
htmlFile.write("         (EE) error\n\n")

slot = os.environ['LCG_NGT_SLT_NAME']
day = os.environ['LCG_NGT_DAY_NAME']
tag = os.environ['LCG_package_config_version']
platform = os.environ['CMTCONFIG']

testDir = '/spi/aaLibrarian/nightlies/' + platform + '/' + slot + '.' + day + '_' + tag + '-' + platform + '/res/'
refDir  = '/spi/aaLibrarian/nightlies/' + platform + '/' + slot + '.' + tag + '-' + platform + '_reference/res/'
for line in logFile:
    temp = re.match(r"(\s+)(\S+)(\s*)(:\s+)(PASS|FAIL|UNTESTED)", line)
    if not temp:
        htmlFile.write(line)
        continue

    splitHeader = temp.groups()
    if(splitHeader[4] == 'PASS'):
        color = '#008000'
    elif(splitHeader[4] == 'FAIL'):
        color = '#FF0000'
    else:
        color = '#FFA500'
    htmlFile.write("%s%s%s%s<font color=\"%s\">%s</font>\n" %
            (splitHeader[0], splitHeader[1],
             splitHeader[2], splitHeader[3], color, splitHeader[4]))

    testName = splitHeader[1].lower()
    test_total_file = testDir + 'total/' + testName + '.log'
    test_live_file  = testDir + 'live/' + testName + '.log'
    test_perf_file  = testDir + 'perf/' + testName + '.log'
    ref_total_file  = refDir + 'total/' + testName + '.log'
    ref_live_file   = refDir + 'live/' + testName + '.log'
    ref_perf_file   = refDir + 'perf/' + testName + '.log'

    htmlFile.write('  [Test files:      <a href="%s">Total Memory</a> <a href="%s">Live Memory</a> <a href="%s">Performance</a>]\n' % (test_total_file, test_live_file, test_perf_file))
    htmlFile.write('  [Reference files: <a href="%s">Total Memory</a> <a href="%s">Live Memory</a> <a href="%s">Performance</a>]\n\n' % (ref_total_file, ref_live_file, ref_perf_file))

htmlFile.write("</pre>\n</body>\n</html>")
htmlFile.close()
logFile.close()
