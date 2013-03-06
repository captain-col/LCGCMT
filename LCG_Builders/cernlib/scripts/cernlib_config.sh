#!/bin/sh

cd ${LCG_builddir}
tar xvfz cernlib-${LCG_CERN_LEVEL}-patches.tar.gz
mkdir cernlib
cd cernlib
tar xvfz ../${LCG_tarfilename}

for ffile in `ls *.gz`; do tar xvfz $ffile; done

if [ x${LCG_LINUXCF_PATCH} != x ] ; then patch -p0 < ../cernlib-${LCG_CERN_LEVEL}-patches/${LCG_LINUXCF_PATCH} ; fi
if [ x${LCG_PLAT_PATCH} != x ]    ; then patch -p0 < ../cernlib-${LCG_CERN_LEVEL}-patches/${LCG_PLAT_PATCH} ; fi
if [ x${LCG_WITHSHIFT_PATCH} != x ]; then echo "# define CERNLIB_SHIFT YES" >> ${LCG_CERN_LEVEL}/src/config/${LCG_WITHSHIFT_PATCH} ; fi
