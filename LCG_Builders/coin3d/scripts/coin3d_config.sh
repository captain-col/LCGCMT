#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd Coin-${LCG_package_config_version}
patch -p0 <Coin-3.1.3.patch
${LCG_coin3d_compile_opts}
./configure --prefix=${LCG_destbindir} ${LCG_coin3d_config_opts}
