#!/bin/sh

cd ${LCG_builddir}/david_${LCG_package_config_version}
mkdir -p ${LCG_extdir}/david/${LCG_package_config_version}/${LCG_CMTCONFIG}/bin
rsync -avz david ${LCG_extdir}/david/${LCG_package_config_version}/${LCG_CMTCONFIG}/bin
