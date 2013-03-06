#!/bin/sh

cd ${LCG_tmpbuild}
tar xvfz ${LCG_tardir}/${LCG_package}-${LCG_package_config_version}.tar.gz
cd ${LCG_package}-${LCG_package_config_version}
python ./configure.py ${LCG_configopts}
