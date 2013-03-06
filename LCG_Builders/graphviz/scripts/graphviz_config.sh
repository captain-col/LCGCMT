#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd graphviz-${LCG_package_config_version}
./configure --prefix=${LCG_extdir}/graphviz/${LCG_package_config_version}/${LCG_CMTCONFIG} ${LCG_graphviz_config_opts}
