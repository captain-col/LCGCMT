#!/bin/sh

cd ${LCG_builddir}/opt/d-cache
mkdir -p ${LCG_destbindir}
rsync -avz . ${LCG_destbindir}
if [[ $CMTCONFIG == *slc6* ]]; then
    mkdir -p ${LCG_destbindir}/dcap
    rsync -avz ../../usr/ ${LCG_destbindir}/dcap/
fi
