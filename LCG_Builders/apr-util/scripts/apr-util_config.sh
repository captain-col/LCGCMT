#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd ${LCG_package}-${LCG_package_config_version}
${LCG_apr-util_compile_options}
./configure --with-apr=${LCG_apr_home} --prefix=${LCG_destbindir}
