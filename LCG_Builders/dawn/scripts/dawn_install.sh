#!/bin/sh

cd ${LCG_destbindir}/dawn_${LCG_package_config_version}
mkdir -p ${LCG_destbindir}/bin
make install INSTALL_DIR=${LCG_destbindir}/bin
