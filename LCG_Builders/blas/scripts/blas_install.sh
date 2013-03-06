#!/bin/sh

cd ${LCG_builddir}/BLAS
mkdir -p ${LCG_destbindir}/lib
if [[ $CMTCONFIG == *mac* ]]; then
    cp arch/*.a shlib/*.so ${LCG_destbindir}/lib
else 
    cp -d arch/*.a shlib/*.so ${LCG_destbindir}/lib
fi
