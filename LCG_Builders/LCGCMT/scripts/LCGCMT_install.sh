#!/bin/sh

date

# create the packagedict.xml file for e.g. further scram integration
cd ${LCG_builddir}/LCGCMT/${LCG_package_config_version}/pyLCG/cmt
CMTEXTRATAGS= cmt run python ../python/lcg/aa/make_packageroots_xml.py -l `pwd`/../..

#Install LCGCMT on AFS 
cd ${LCG_builddir}/LCGCMT/${LCG_package_config_version}/
afsdir=`echo ${LCG_reldir} | sed -e  's,build,afs/cern.ch/sw/lcg/app,'` 
mkdir -p ${afsdir}/LCGCMT/${LCG_package_config_version}

tar -cf -  * | (cd  ${afsdir}/LCGCMT/${LCG_package_config_version}; tar -xf - )

# generate setup scripts in the install area (for ATLAS only for the time being)
cd ${afsdir}/LCGCMT/${LCG_package_config_version}/LCG_Release/cmt
cmt -tag_add=ATLAS gen_setup_scripts
cmt -tag_add=ATLAS make
