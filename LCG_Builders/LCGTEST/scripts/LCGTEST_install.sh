#!/bin/sh

cd ${LCG_builddir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}/src/config/cmt
cmt broadcast -global -select="/${LCG_package_config_version}/" rm -fr ../${LCG_CMTCONFIG}
cd ../../..

afsdir=`echo ${LCG_reldir} | sed -e  's,build,afs/cern.ch/sw/lcg/app,' `
mkdir -p ${afsdir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}

if [ ! -d ${afsdir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}/src ]; then src=src; fi
tar -cf -   $src include ${LCG_CMTCONFIG} | (cd  ${afsdir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}; tar -xf - )
