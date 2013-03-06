#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tardir}/${LCG_package}-${LCG_package_config_version}.tar.gz
cd ${LCG_package}-${LCG_package_config_version}
./configure ${LCG_configopts}
