#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd expat-${LCG_package_config_version}
${LCG_expat_compile_options}
./configure --prefix=${LCG_extdir}/expat/${LCG_package_config_version}/${LCG_CMTCONFIG}
