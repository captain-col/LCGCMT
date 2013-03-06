#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd rx-${LCG_package_config_version}
./configure --prefix=${LCG_extdir}/rx/${LCG_package_config_version}/${LCG_CMTCONFIG}