#!/bin/sh
 
cd ${LCG_builddir}/${LCG_package_config_version}

afsdir=`echo ${LCG_reldir} | sed -e  's,build,afs/cern.ch/sw/lcg/app,' | sed -e 's,scratch,afs/cern.ch/sw/lcg/app,' `

mkdir -p ${afsdir}/${LCG_package_config_version}

#if [ -d ${afsdir}/SEAL/${LCG_package_config_version}/src ]; then src=src; fi

tar -cf - geant4  | (cd  ${afsdir}/${LCG_package_config_version}; tar -xf - )
