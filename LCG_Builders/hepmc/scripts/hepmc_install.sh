#!/bin/sh

cd ${LCG_builddir}/HepMC-${LCG_package_config_version}
mkdir -p {LCG_extdir}/HepMC/${LCG_package_config_version}/${LCG_CMTCONFIG}
make install
