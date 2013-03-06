#!/bin/sh

cd ${LCG_builddir}/dawn_${LCG_package_config_version}
mkdir -p ${LCG_extdir}/dawn/${LCG_package_config_version}/${LCG_CMTCONFIG}/bin
make install INSTALL_DIR=${LCG_extdir}/dawn/${LCG_package_config_version}/${LCG_CMTCONFIG}/bin
