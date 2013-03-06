#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tardir}/${LCG_tarfilename}
mkdir ${LCG_package}-${LCG_package_config_version}-obj
cd ${LCG_package}-${LCG_package_config_version}-obj
eval ${LCG_gcc_config_pre_opts} ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}/configure --prefix=${LCG_extdir}/${LCG_package}/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_gcc_config_post_opts}
