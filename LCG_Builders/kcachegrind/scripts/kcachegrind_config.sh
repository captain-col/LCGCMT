#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd kcachegrind-${LCG_package_config_version}
./configure --prefix=${LCG_extdir}/kcachegrind/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_kcachegrind_config_extra_opts}
