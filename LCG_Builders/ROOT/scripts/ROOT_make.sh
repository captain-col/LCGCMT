#!/bin/sh

# Set the maximum load during the job.  This can be overridden in the
# environment.
if [ "x$LCG_MAX_LOAD" = "x" ]; then
    LCG_MAX_LOAD=2.5
fi
echo Limit load to ${LCG_MAX_LOAD}

which sysctl
echo $PATH
date
cd ${LCG_builddir}/ROOT/${LCG_CheckoutDir}/root
svn info
if [ $# == 1 ]; then
    #if code coverage is "turned on" compile with special OPT parameters
    if [[ ! -z "$GCOV_TOOL" ]];then
        make -k -l ${LCG_MAX_LOAD} -j$1 OPT="-fprofile-arcs -ftest-coverage"
    else
        make -k -l ${LCG_MAX_LOAD} -j$1
    fi
    cd test
    make -k -l ${LCG_MAX_LOAD} -j$1
    date
else
    #if code coverage is "turned on" compile with special OPT parameters
    if [[ ! -z "$GCOV_TOOL" ]];then
        make -k -l ${LCG_MAX_LOAD} -j OPT="-fprofile-arcs -ftest-coverage"
    else
        make -k -l ${LCG_MAX_LOAD} -j
    fi
    cd test
    make -k -l ${LCG_MAX_LOAD} -j
    date
fi
