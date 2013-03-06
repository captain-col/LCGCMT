#!/bin/sh

cd ${LCG_builddir}/libpfm-${LCG_package_config_version}
DESTDIR=${LCG_destbindir} make install
