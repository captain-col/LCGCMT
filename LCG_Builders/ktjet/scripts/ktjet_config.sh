#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd KtJet-${LCG_package_config_version}
${LCG_ktjet_compile_options}
./configure --with-clhep=${LCG_clhep_root} --with-clhep_vector-libpath=${LCG_clhep_root}/lib --prefix=${LCG_extdir}/ktjet/${LCG_package_config_version}/${LCG_CMTCONFIG}
