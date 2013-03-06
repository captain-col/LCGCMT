#!/bin/sh

cd ${LCG_builddir}/frontier_client__${LCG_package_config_version}__src/dist
LCG_PKG_DEST=${LCG_extdir}/frontier_client/${LCG_package_config_version}/${LCG_CMTCONFIG}
if [ ! -d ${LCG_PKG_DEST} ] ; then
 mkdir -p ${LCG_extdir}/frontier_client/${LCG_package_config_version}/${LCG_CMTCONFIG}
fi
cp -r * ${LCG_PKG_DEST}
