#!/bin/sh

cd ${LCG_builddir}/ROOT/${LCG_CheckoutDir}/root

afsdir=`echo ${LCG_reldir} | sed -e  's,build,afs/cern.ch/sw/lcg/app,' `

mkdir -p ${afsdir}/ROOT/${LCG_package_native_version}/${LCG_CMTCONFIG}

find . -name '*.[od]' | xargs rm

cd ..
tar -cf -   root | (cd  ${afsdir}/ROOT/${LCG_package_native_version}/${LCG_CMTCONFIG}; tar -xf - )

