#!/bin/sh
date
cd ${LCG_builddir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}/GaudiRelease/cmt

if [ "x${CMTEXTRATAGS}" = "x" ] ; then export CMTEXTRATAGS="ATLAS" ; else export CMTEXTRATAGS="ATLAS,${CMTEXTRATAGS}"; fi

cmt show uses
cmt broadcast  -global -select="/${LCG_package_config_version}/"  cmt config
