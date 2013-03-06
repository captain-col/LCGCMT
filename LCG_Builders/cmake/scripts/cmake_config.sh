#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd cmake-${LCG_package_config_version}
eval "${LCG_cmake_compile_options}"
./configure --prefix=${LCG_extdir}/CMake/${LCG_package_config_version}/${LCG_CMTCONFIG}
