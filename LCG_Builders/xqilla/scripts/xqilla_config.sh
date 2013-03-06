#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd ${LCG_builddir}/XQilla-${LCG_package_config_version}
./configure --prefix=${LCG_extdir}/xqilla/${LCG_package_config_version}/${LCG_CMTCONFIG} --with-xerces=${LCG_extdir}/XercesC/${LCG_xercesc_config_version}/${LCG_CMTCONFIG} --disable-rpath

