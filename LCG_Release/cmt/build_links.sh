#!/bin/sh
#
# build_links.sh
#
# Description:-
#   Script to build library links for all platforms for LCGCMT. It 
#   assumes that the initial environment is setup correctly, and that 
#   the script is executed in the LCG_Release/cmt directory. It uses 
#   ATLAS-specific values of CMTCONFIG.
#
# Author:-
#   David Quarrie <David.Quarrie@cern..ch>

function build_platform_links( ) {
    echo "Now working on ${CMTCONFIG}..."
    if [ -f build-${CMTCONFIG}.log ]; then
        rm -f build-${CMTCONFIG}.log
    fi
    python ../../LCG_Settings/python/lcg_InstallArea.py >& build-${CMTCONFIG}.log
}

s_configs="i686-slc5-gcc43 x86_64-slc5-gcc43 i386-mac105-gcc40 i386-mac106-gcc42 x86_64-mac106-gcc42"
for s_config in `echo ${s_configs}`; do
    export CMTCONFIG=${s_config}-dbg
    build_platform_links
    export CMTCONFIG=${s_config}-opt
    build_platform_links
done
echo "All done"


