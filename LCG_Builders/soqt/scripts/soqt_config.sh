#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd SoQt-${LCG_package_config_version}
${LCG_soqt_compile_opts}
./configure --prefix=${LCG_destbindir} ${LCG_soqt_config_opts}
