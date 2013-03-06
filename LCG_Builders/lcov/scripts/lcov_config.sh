#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
ls
#cp ${LCG_difffiledir} ${LCG_builddir}/lcov-${LCG_package_config_version}
#cd ${LCG_builddir}/lcov-${LCG_package_config_version}
#tar xvfz ${LCG_tardiffname}
#patch -p0 < Makefile.diff
#patch -p0 < bin.install.diff
