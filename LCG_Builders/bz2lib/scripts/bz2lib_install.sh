#!/bin/sh

cd ${LCG_builddir}/bzip2-${LCG_package_config_version}
make install PREFIX=${LCG_extdir}/bz2lib/${LCG_package_config_version}/${LCG_CMTCONFIG}