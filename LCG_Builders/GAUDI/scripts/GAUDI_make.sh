#!/bin/sh
date

echo
echo "g++ location: " `which g++`
g++ --version
echo

cd ${LCG_builddir}/GAUDI/${LCG_package_config_version}/GaudiRelease/cmt
cmt show uses

if [ $# == 2 ]; then

sh ${LCG_BUILDPOLICYROOT_DIR}/scripts/tbroadcast_make.sh $1 $2 all utilities tests

else

cmt broadcast -global -select="/${LCG_package_config_version}/" - cmt make all_groups

fi

date
