#!/bin/sh
date
cd ${LCG_builddir}/RELAX/${LCG_package_config_version}/src/config/cmt
# code coverage is not turned on, we can execute following command
[[ -z $GCOV_TOOL ]] && cmt broadcast -global -select="/${LCG_package_config_version}/" rm -fr ../${LCG_CMTCONFIG}
cd ../../..
afsdir=`echo ${LCG_reldir} | sed -e  's,build,afs/cern.ch/sw/lcg/app,' `

mkdir -p ${afsdir}/RELAX/${LCG_package_config_version}
if [ ! -d ${afsdir}/RELAX/${LCG_package_config_version}/src ]; then src=src; fi

tar -cf -   $src include ${LCG_CMTCONFIG} | (cd  ${afsdir}/RELAX/${LCG_package_config_version}; tar -xf - )

cd ${afsdir}/COOL/${LCG_package_config_version}
ln -sf $LCG_CMTCONFIG $ATLAS_TAGS_MAP

date
