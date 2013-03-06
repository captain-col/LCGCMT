#!/bin/sh

cd ${LCG_builddir}
tar xvfz ${LCG_tarfilename}

cp ${LCG_extdir}/tarFiles/${LCG_tardiffname} ./
tar xvfz ${LCG_tardiffname}
patch -c ${LCG_qt_pkgname}/src/gui/kernel/qapplication_mac.mm qtmac.patch

cd ${LCG_qt_pkgname}
eval ${LCG_qt_pre_config_step}
./configure ${LCG_qt_extra_config_opts} -no-separate-debug-info -release --prefix=${LCG_extdir}/${LCG_package}/${LCG_package_config_version}/${LCG_CMTCONFIG} -nomake examples -nomake demos <<EOF
o
yes
EOF
