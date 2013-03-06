#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
${LCG_doxygen_pre_config_step}
cd doxygen-${LCG_package_config_version}
./configure --prefix ${LCG_extdir}/doxygen/${LCG_package_config_version}/${LCG_CMTCONFIG}
