#!/bin/sh

cd ${LCG_builddir}/rx-${LCG_package_config_version}
LCG_PKG_DEST=${LCG_extdir}/rx/${LCG_package_config_version}/${LCG_CMTCONFIG}
if [ ! -d ${LCG_PKG_DEST} ] ; then mkdir -p ${LCG_PKG_DEST}; fi 
make install
