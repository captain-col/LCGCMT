#!/bin/sh

cd ${LCG_builddir}/lcov-${LCG_package_config_version}
make install PREFIX=${LCG_destbindir}
mv ${LCG_destbindir}/usr/bin ${LCG_destbindir}
mv ${LCG_destbindir}/usr/share/man ${LCG_destbindir}
rmdir ${LCG_destbindir}/usr/share
rmdir ${LCG_destbindir}/usr
