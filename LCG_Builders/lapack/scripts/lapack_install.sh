#!/bin/sh

cd ${LCG_builddir}/${LCG_package}-${LCG_package_config_version}
mkdir -p ${LCG_destbindir}
cp -r lib ${LCG_destbindir}

