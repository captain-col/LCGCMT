#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd fftw-${LCG_package_config_version}
CFLAGS=" -fPIC " ./configure --enable-shared --prefix=${LCG_extdir}/fftw3/${LCG_package_config_version}/${LCG_CMTCONFIG}
