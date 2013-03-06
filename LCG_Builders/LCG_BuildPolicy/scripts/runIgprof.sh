#!/bin/bash

#
# Auth: Ilias Tsitsimpis
#       (Summer Student)
# Date: August 2011
#
# Script to run igprof for every test and examine the results
# It takes 3 arguments
#    the name of the test
#    the name of the executable
#    the arguments to that executable
#
######################################################################

TEST_FILE=`echo $1 | tr '[A-Z]' '[a-z]'`

# Run igprof as memory profiler
igprof -mp -z -o $IGPROF_TEST_RES/raw/mem/$TEST_FILE.mp.gz $2 >& /dev/null
# Run igprof as performance profiler
igprof -pp -z -o $IGPROF_TEST_RES/raw/perf/$TEST_FILE.pp.gz $2 >& /dev/null

# Examine MEM_TOTAL from memory results
igprof-analyse -d -v -g -r MEM_TOTAL $IGPROF_TEST_RES/raw/mem/$TEST_FILE.mp.gz >& $IGPROF_TEST_RES/res/total/$TEST_FILE.log
# Examine MEM_LIVE from memory results
igprof-analyse -d -v -g -r MEM_LIVE $IGPROF_TEST_RES/raw/mem/$TEST_FILE.mp.gz >& $IGPROF_TEST_RES/res/live/$TEST_FILE.log
# Examine data from performance results
igprof-analyse -d -v -g $IGPROF_TEST_RES/raw/perf/$TEST_FILE.pp.gz >& $IGPROF_TEST_RES/res/perf/$TEST_FILE.log


#
# Use analyzeIgprof.py script to analyse our results
# Compare them with some reference files to report PASS or FAIL
#

# Analyze results for memory leaks
analyzeIgprof.py MemLive $IGPROF_TEST_RES/res/live/$TEST_FILE.log
# Analyze results for total memory use of each function
analyzeIgprof.py MemTotal $IGPROF_TEST_RES/res/total/$TEST_FILE.log $IGPROF_REF_RES/res/total/$TEST_FILE.log
# Analyze results for performance in time of each function
analyzeIgprof.py Perf $IGPROF_TEST_RES/res/perf/$TEST_FILE.log $IGPROF_REF_RES/res/perf/$TEST_FILE.log
