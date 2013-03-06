#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd HepMC-${LCG_package_config_version}
./configure --prefix=${LCG_extdir}/HepMC/${LCG_package_config_version}/${LCG_CMTCONFIG} --with-momentum=MEV --with-length=MM ${LCG_hepmc_config_options}
