#!/bin/sh

cd ${LCG_builddir}
if [ x"${LCG_ONLY_ROOFIT}" = x"NO" ] ; then tar xvfz root_v${LCG_root_version}.source.tar.gz ; fi
rm -fr root/roofit
tar xvfz ${LCG_tarfilename}
if [ x"${LCG_WITH_MATHCORE}" = x"YES" ] ; then 
    rm -fr root/math/mathcore
    tar xvfz mathcore_root_${LCG_mathcore_version}.tar.gz ; 
fi
cd root
./configure ${LCG_ROOT_CONFIG_ARCH} --enable-roofit --prefix=`pwd`

