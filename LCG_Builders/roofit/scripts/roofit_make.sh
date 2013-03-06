#!/bin/sh

cd ${LCG_builddir}/root
if [ "x${LCG_WITH_MATHCORE}" == "xYES" ] ; then 
    make all-mathcore -j12 ; 
fi
make all-roofitcore all-roofit all-roostats -j12

