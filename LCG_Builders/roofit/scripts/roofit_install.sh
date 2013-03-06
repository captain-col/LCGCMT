#!/bin/sh

cd ${LCG_builddir}/root
mkdir -p ${LCG_destbindir}/lib
rsync -avz lib/libRooFit* lib/libRooStats* ${LCG_destbindir}/lib
mkdir -p ${LCG_destbindir}/include
rsync -avz lib/libRooFit* lib/libRooStats* ${LCG_destbindir}/lib
rsync -avz --exclude "*LinkDef*" roofit/roofitcore/inc/* roofit/roofit/inc/* roofit/roostats/inc/* ${LCG_destbindir}/include
rsync -avz roofit/doc ${LCG_destbindir}/
if [ "x${LCG_WITH_MATHCORE}" = "xYES" ] ; then 
    rsync -avz lib/libMath* ${LCG_destbindir}/lib ; 
    rsync -avz math/mathcore/inc/* ${LCG_destbindir}/include ; 
fi
