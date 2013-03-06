#!/bin/sh

cd ${LCG_builddir}/GAUDI/${LCG_package_config_version}

afsdir=`echo ${LCG_reldir} | sed -e  's,build,afs/cern.ch/sw/lcg/app,' `
mkdir -p ${afsdir}/GAUDI/${LCG_package_config_version}

if [ ! -d ${afsdir}/GAUDI/${LCG_package_config_version}/Gaudi ]; then
  tar --exclude "*.o" -cf -  * | (cd  ${afsdir}/GAUDI/${LCG_package_config_version}; tar -xf - )
else 
  tar --exclude "*.o" -cf - */${LCG_CMTCONFIG}/* | (cd ${afsdir}/GAUDI/${LCG_package_config_version}; tar -xf - )
fi
