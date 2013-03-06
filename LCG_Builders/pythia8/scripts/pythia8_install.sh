#!/bin/sh

cd ${LCG_builddir}/${LCG_package}/${LCG_package_config_version}

afsdir=`echo ${LCG_reldir} | sed -e  's,build,afs/cern.ch/sw/lcg/app,' `

mkdir -p ${afsdir}/${LCG_package}/${LCG_package_config_version}/${LCG_CMTCONFIG}
if [ ! -d ${afsdir}/${LCG_pacakge}/${LCG_package_config_version}${LCG_CMTCONFIG}/src ]; then src=src; fi

tar -cf -   $src include lib | (cd  ${afsdir}/${LCG_package}/${LCG_package_config_version}/${LCG_CMTCONFIG}; tar -xf - )
