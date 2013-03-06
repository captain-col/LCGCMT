#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd ${LCG_package}-${LCG_package_config_version}
${LCG_apr_compile_options}
./configure --prefix=${LCG_destbindir}
