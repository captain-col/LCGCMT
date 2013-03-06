#!/bin/sh

which sysctl
echo $PATH
date
cd ${LCG_builddir}/ROOT/${LCG_CheckoutDir}/root
svn info
if [ $# == 1 ]; then
    #if code coverage is "turned on" compile with special OPT parameters
    if [[ ! -z "$GCOV_TOOL" ]];then
        make -k -j$1 OPT="-fprofile-arcs -ftest-coverage"
    else
        make -k -j$1
    fi
    cd test
    make -k -j$1
    
    date


else
    #if code coverage is "turned on" compile with special OPT parameters
    if [[ ! -z "$GCOV_TOOL" ]];then
        make -k -j4 OPT="-fprofile-arcs -ftest-coverage"
    else
        make -k -j4
    fi
    cd test
    make -k -j3
    date
fi
