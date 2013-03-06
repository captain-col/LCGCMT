#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd gsl-${LCG_package_config_version}
CFLAGS=" -O2 " ./configure --prefix=${LCG_extdir}/GSL/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_gsl_config_opts}
