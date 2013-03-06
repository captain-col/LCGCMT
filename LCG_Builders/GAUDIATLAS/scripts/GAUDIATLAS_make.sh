#!/bin/sh
date

if [ "x${CMTEXTRATAGS}" == "x" ] ; then export CMTEXTRATAGS="ATLAS" ; else export CMTEXTRATAGS="ATLAS,${CMTEXTRATAGS}"; fi

cd ../../../LCG_Release/cmt
cmt python-build

cd ${LCG_builddir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}/GaudiRelease/cmt
cmt show uses
date
if [ $# == 2 ]; then

sh ${LCG_BUILDPOLICYROOT_DIR}/scripts/tbroadcast_make.sh $1 $2 all utilities tests

else

cmt broadcast -global -select="/${LCG_package_config_version}/" - cmt make all_groups

fi
