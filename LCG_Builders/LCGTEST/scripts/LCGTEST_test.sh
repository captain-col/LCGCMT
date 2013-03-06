#!/bin/sh

cd ${LCG_builddir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}/src/config/cmt
. ./setup.sh
cd ../qmtest

date > ../../../logs/$CMTCONFIG-qmtest.log
qmtest run -o ../../../logs/$CMTCONFIG-qmtest-results.qmr >> ../../../logs/$CMTCONFIG-qmtest.log
qmtest summarize -f brief ../../../logs/$CMTCONFIG-qmtest-results.qmr >> ../../../logs/$CMTCONFIG-qmtest.log
date >> ../../../logs/$CMTCONFIG-qmtest.log
