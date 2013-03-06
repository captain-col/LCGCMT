#!/bin/sh

cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}
make install
cd ${LCG_destbindir}
ln -s lib lib64
