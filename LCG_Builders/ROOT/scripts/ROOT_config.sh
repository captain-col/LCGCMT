#!/bin/sh
date
cd ${LCG_builddir}/ROOT/${LCG_CheckoutDir}
if [ -d root -a -f  ./${LCG_tarfilename} ]; then 
	tar xvfz ${LCG_tarfilename}
fi

COVLD=""
#If coverage testing is configured, configure ROOT with differend linker. This linker just calls g++ with lgcov at the end.
if [[ ! -z "$GCOV_TOOL" ]];then
	COVLD="--with-ld=${LCG_package_root}/scripts/root_gcovld.sh"
fi

cd root
eval "./configure ${LCG_ROOT_CONFIG_ARCH} ${LCG_ROOT_CONFIG_OPTIONS} ${COVLD}"  #--prefix=${LCG_extdir}/root/${LCG_package_config_version}/${LCG_CMTCONFIG}
