#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd google-perftools-${LCG_package_config_version}

 ./configure --prefix=${LCG_extdir}/tcmalloc/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_tcmalloc_config_opts} 
