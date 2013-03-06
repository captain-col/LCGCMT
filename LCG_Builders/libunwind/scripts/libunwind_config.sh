#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd libunwind-${LCG_package_config_version}
autoreconf -i
 ./configure --prefix=${LCG_extdir}/libunwind/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_libunwind_config_opts} 
