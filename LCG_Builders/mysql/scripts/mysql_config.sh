#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
LCG_mysqldir=${LCG_extdir}/mysql/${LCG_package_config_version}/${LCG_CMTCONFIG}
${LCG_mysql_compile_options}
cd mysql-${LCG_package_config_version}
cmake -DCMAKE_INSTALL_PREFIX:PATH=${LCG_destbindir}
#./configure --prefix=${LCG_destbindir}
