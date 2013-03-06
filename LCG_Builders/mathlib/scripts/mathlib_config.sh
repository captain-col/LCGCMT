#!/bin/sh

cd ${LCG_builddir}
tar xvfz root_v${LCG_root_version}.source.tar.gz
tar xvfz ${LCG_tarfilename}
cd root
./configure ${LCG_ROOT_CONFIG_ARCH} --enable-mathmore --with-gsl-incdir=${LCG_GSLROOT}/include --with-gsl-libdir=${LCG_GSLROOT}/lib --enable-minuit2 --prefix=`pwd`
