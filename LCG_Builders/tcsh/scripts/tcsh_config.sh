#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd tcsh-${LCG_package_config_version}
./configure --prefix=${LCG_extdir}/tcsh/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_tcsh_config_opts}
