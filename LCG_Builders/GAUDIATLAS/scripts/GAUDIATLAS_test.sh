#!/bin/sh

LOGFILE=${LCG_builddir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}/logs/$LCG_CMTCONFIG-qmtest.log
COVFILE=${LCG_builddir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}/logs/$LCG_CMTCONFIG-coverage.log
if [ x$LCG_IsCernVM == "xyes" ]; then
        LOGFILE=$LCG_CernVMSumfile
	COVFILE=$LCG_CernVMCovfile
else
	if [[ ! -d ${LCG_builddir}/GAUDIATLAS/${LCG_package_config_version}/logs ]]
	then
        	echo "logs directory in GAUDIATLAS project does not exists..creating." 
       		mkdir ${LCG_builddir}/GAUDIATLAS/${LCG_package_config_version}/logs
	fi
fi

date > $LOGFILE
cd ${LCG_builddir}/${LCG_pkgdest_pkgname}/${LCG_package_config_version}/GaudiRelease/cmt
if [ "x${CMTEXTRATAGS}" == "x" ] ; then export CMTEXTRATAGS="ATLAS" ; else export CMTEXTRATAGS="ATLAS,${CMTEXTRATAGS}"; fi

#cmt broadcast -global -select="/${LCG_package_config_version}/" cmt qmtest_run
cmt qmtest_summarize >> $LOGFILE 2>&1
date >> $LOGFILE


# code coverage
[[ ! -z $GCOV_TOOL ]] && bash ${LCG_BUILDPOLICYROOT_DIR}/scripts/pkg_coverage.sh 2>&1 > $COVFILE

