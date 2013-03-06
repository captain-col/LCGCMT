#!/bin/sh
date
cd ${LCG_builddir}/COOL/${LCG_package_config_version}/src/config/cmt


if [ $# == 2 ]; then

sh ${LCG_BUILDPOLICYROOT_DIR}/scripts/tbroadcast_make.sh $1 $2 all utilities tests

else
 cmt broadcast -global -select="/${LCG_package_config_version}/" - cmt make --debug all_groups

fi


${COOL_post_make_step}

. setup.sh ""
export QUIET_ASSERT=a 
export SEAL_KEEP_MODULES=1 

g++ --version
date

