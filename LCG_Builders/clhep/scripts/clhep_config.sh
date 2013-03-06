#!/bin/sh


cd ${LCG_builddir}
mkdir clhep
cd clhep
tar xvfz ../${LCG_tarfilename}
echo ${LCG_clhep_version}
cd ${LCG_clhep_version}
mkdir build
cd build
../CLHEP/configure --prefix=${LCG_extdir}/clhep/${LCG_clhep_version}/${LCG_CMTCONFIG}
