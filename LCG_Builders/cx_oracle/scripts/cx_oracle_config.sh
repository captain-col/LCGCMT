#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}
cd ${LCG_builddir}/cx_Oracle-${LCG_package_config_version}
patch -p0 < ../cx_Oracle-${LCG_package_config_version}.diff
