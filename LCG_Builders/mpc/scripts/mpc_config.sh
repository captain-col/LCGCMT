#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd mpc-${LCG_package_config_version}
./configure --with-mpfr=${LCG_mpfr_home} --with-gmp=${LCG_gmp_home} --prefix=${LCG_destbindir} 
