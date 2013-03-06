#!/bin/sh
cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd libpng-${LCG_package_config_version}
./configure --prefix=${LCG_extdir}/libpng/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_libpng_config_opts}
