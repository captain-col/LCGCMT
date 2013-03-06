#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd sqlite-autoconf-${LCG_package_config_version}
${LCG_sqlite_compile_options}
 ./configure --prefix=${LCG_destbindir}
