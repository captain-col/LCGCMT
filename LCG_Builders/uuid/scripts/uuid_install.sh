#!/bin/sh

cd ${LCG_builddir}/e2fsprogs-${LCG_package_config_version}/lib/uuid
mkdir -p ${LCG_destbindir}
make install
